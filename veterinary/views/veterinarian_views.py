from rest_framework import generics, permissions, authentication

from ..models import Veterinarian, MedicalCenter
from ..serializers import veterinarian_serializer


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
