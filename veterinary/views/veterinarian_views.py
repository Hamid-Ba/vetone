from django_filters.rest_framework import DjangoFilterBackend
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from rest_framework import (
    views,
    generics,
    permissions,
    authentication,
    response,
    status,
)

from config.pagination import StandardPagination
from monitoring.models.observability import CodeLog

from ..services import rancher_services
from ..filters import VeterinarianFilter
from ..models import Veterinarian, MedicalCenter, Rancher
from ..serializers import veterinarian_serializer, rancher_serializer, serializers


class RegisterVeterinarianAPI(generics.CreateAPIView):
    """Register Veterinarian API"""

    queryset = Veterinarian.objects.all()
    serializer_class = veterinarian_serializer.RegisterVeterinarianSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        """Register Veterinarian"""
        user = self.request.user

        # Get fullName and image from request data
        fullName = serializer.validated_data.get("fullName")
        image = serializer.validated_data.get("image")

        # If User's fullName is empty, update it
        if not user.fullName and fullName:
            user.fullName = fullName
            user.save(update_fields=["fullName"])

        # If User's image is empty, update it
        if not user.image and image:
            user.image = image
            user.save(update_fields=["image"])

        # Set slug: Use updated fullName if available, otherwise use phone
        slug = slugify(user.fullName) if user.fullName else slugify(user.phone)

        return serializer.save(user=user, slug=slug)


class MedicalCenterListAPI(generics.ListAPIView):
    """Medical Center List API"""

    queryset = MedicalCenter.objects.all()
    serializer_class = veterinarian_serializer.MedicalCenterSerializer


class RancherListAPI(generics.ListAPIView):
    """Rancher List API"""

    queryset = Rancher.objects.order_by("-id")
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = StandardPagination
    serializer_class = rancher_serializer.RancherVeterinarianSerializer

    def get_queryset(self):
        return self.queryset.filter(veterinarians__user=self.request.user)


class AddRancherAPI(views.APIView):
    """Add Rancher API"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    class AddRancherInputSerializer(serializers.Serializer):
        """Add Rancher Input Serializer"""

        fullName = serializers.CharField(required=True)
        phone = serializers.CharField(required=True)
        village_name = serializers.CharField(required=True)
        city_id = serializers.IntegerField(required=True)

    @extend_schema(
        request=AddRancherInputSerializer,
        responses=rancher_serializer.RancherSerializer,
    )
    def post(self, request, *args, **kwargs):
        input_data = self.AddRancherInputSerializer(data=self.request.data, many=False)
        input_data.is_valid(raise_exception=True)

        if Rancher.objects.filter(user__phone=input_data.data["phone"]).exists():
            return response.Response(
                {"message": "Rancher has been added already!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            rancher = rancher_services.add_rancher(
                veterinarian_user=self.request.user, **input_data.data
            )
        except Exception as e:
            CodeLog.log_critical(
                "veteinarian_views.py",
                "class AddRancherAPI",
                str(e),
                {"user_phone": self.request.user.phone},
            )
            return response.Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response.Response(
            rancher_serializer.RancherSerializer(rancher, many=False).data,
            status=status.HTTP_201_CREATED,
        )


class RemoveRancherAPI(views.APIView):
    """Remove Rancher API"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def delete(self, request, phone: str, *args, **kwargs):

        rancher = Rancher.objects.filter(user__phone=phone).first()

        if not rancher:
            return response.Response(
                {"message": "Rancher does not exist!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            is_removed = rancher_services.remove_rancher(
                veterinarian_user=self.request.user, rancher=rancher
            )
        except Exception as e:
            CodeLog.log_critical(
                "veteinarian_views.py",
                "class RemoveRancherAPI",
                str(e),
                {"user_phone": self.request.user.phone},
            )
            return response.Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if is_removed:
            return response.Response(
                {"message": "Rancher Removed Successfuly"},
                status=status.HTTP_204_NO_CONTENT,
            )

        CodeLog.log_critical(
            "veteinarian_views.py",
            "class RemoveRancherAPI",
            "is_removed returned False",
            {"rancher": rancher.user.phone},
        )
        return response.Response(
            {"message": "STH Goes Wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SearchVeterinarianAPI(generics.ListAPIView):
    """
    - Example
            •	Full-text search: GET /veterinary/?search=laptop
        •	Filter by price range: GET /veterinary/?price_min=1000&price_max=5000
        •	Filter by stock: GET /veterinary/?stock_min=10&stock_max=100
        •	Order by price: GET /veterinary/?ordering=price
        •	Filter by brand name: GET /veterinary/?brand=Apple
    """

    queryset = Veterinarian.objects.all().select_related("user", "province", "city")
    serializer_class = veterinarian_serializer.VeterinarianSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VeterinarianFilter
    pagination_class = StandardPagination

    # Search configuration
    search_fields = ["user__fullName", "province__name", "city__name"]
    filterset_fields = ["province", "city"]
    ordering_fields = [
        "created_at",
        "updated_at",
    ]

    permission_classes = (permissions.AllowAny,)

    http_method_names = ["get"]
