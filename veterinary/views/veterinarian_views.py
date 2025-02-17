from drf_spectacular.utils import extend_schema
from rest_framework import (
    views,
    generics,
    permissions,
    authentication,
    response,
    status,
)

from monitoring.models.observability import CodeLog

from ..services import rancher_services
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
        return serializer.save(user=self.request.user)


class MedicalCenterListAPI(generics.ListAPIView):
    """Medical Center List API"""

    queryset = MedicalCenter.objects.all()
    serializer_class = veterinarian_serializer.MedicalCenterSerializer


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
