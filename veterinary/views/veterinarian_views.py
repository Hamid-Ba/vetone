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
from django.shortcuts import get_object_or_404

from config.pagination import StandardPagination
from monitoring.models.observability import CodeLog

from ..services import rancher_services, veterinarian_services
from ..filters import VeterinarianFilter
from ..models import Veterinarian, MedicalCenter, Rancher
from ..serializers import veterinarian_serializer, rancher_serializer, serializers


class RegisterVeterinarianAPI(generics.CreateAPIView):
    """Register Veterinarian API"""

    queryset = Veterinarian.objects.all()
    serializer_class = veterinarian_serializer.RegisterVeterinarianSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = self.request.user

        veter = Veterinarian.objects.filter(user=user).first()

        if veter:
            return response.Response(
                {"message": "Veter has been added already!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get fullName and image from request data
        fullName = self.request.data.pop("fullName", None)
        image = self.request.data.pop("image", None)

        # If User's fullName is empty, update it
        if not user.fullName and not fullName:
            return response.Response(
                {"message": "نام کامل خود را وارد کنید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If User's image is empty, update it
        if not user.image and not image:
            return response.Response(
                {"message": "تصویر خود را وارد کنید"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Register Veterinarian"""
        user = self.request.user

        # Get fullName and image from request data
        fullName = serializer.validated_data.pop("fullName", None)
        image = serializer.validated_data.pop("image", None)

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

        veterinarian_services.add_veterinarian_address(
            user=user,
            street=serializer.validated_data.pop("street", None),
            clinic_name=serializer.validated_data.pop("clinic_name", None),
            latitude=serializer.validated_data.pop("latitude", None),
            longitude=serializer.validated_data.pop("longitude", None),
        )

        return serializer.save(user=user, slug=slug)


class VeterinarianAPI(generics.RetrieveUpdateAPIView):
    """Retrieve, Update (PUT/PATCH) Veterinarian API"""

    serializer_class = veterinarian_serializer.VeterinarianSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return veterinarian_serializer.UpdateVeterinarianSerializer
        return veterinarian_serializer.VeterinarianSerializer

    def get_object(self):
        """Return the veterinarian linked to the logged-in user"""
        return self.request.user.veterinarian


class GetVeterinarianAPI(generics.RetrieveAPIView):
    """Retrieve Veterinarian API"""

    queryset = Veterinarian.objects.get_confirmed_veters()
    serializer_class = veterinarian_serializer.VeterinarianSerializer
    lookup_field = "slug"


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
        latitude = serializers.CharField(required=True)
        longitude = serializers.CharField(required=True)

    @extend_schema(
        request=AddRancherInputSerializer,
        responses=rancher_serializer.RancherSerializer,
    )
    def post(self, request, *args, **kwargs):
        input_data = self.AddRancherInputSerializer(data=self.request.data, many=False)
        input_data.is_valid(raise_exception=True)

        rancher = Rancher.objects.filter(user__phone=input_data.data["phone"]).first()
        veterinarian_user = self.request.user

        veterinarian = get_object_or_404(Veterinarian, user=veterinarian_user)

        if veterinarian.state != "C":
            return response.Response(
                {"message": "وضعیت شما تایید نشده است"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if rancher and rancher.veterinarians.contains(self.request.user.veterinarian):
            return response.Response(
                {"message": "Rancher has been added already!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if rancher:
            rancher = rancher_services.add_veterinarian_to_rancher(
                veterinarian_user=veterinarian_user, rancher=rancher
            )
        try:
            rancher = rancher_services.add_rancher(
                veterinarian_user=veterinarian_user, **input_data.data
            )
        except Exception as e:
            CodeLog.log_critical(
                "veteinarian_views.py",
                "class AddRancherAPI",
                str(e),
                {"user_phone": veterinarian_user.phone},
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

    queryset = Veterinarian.objects.filter(state="C", is_active=True).select_related(
        "user", "province", "city"
    )
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
