from rest_framework import serializers

from ..models import Veterinarian, MedicalCenter


class RegisterVeterinarianSerializer(serializers.ModelSerializer):
    """Register Veterinarian Serializer"""

    class Meta:
        model = Veterinarian
        fields = [
            "medical_license",
            "license_type",
            "license_image",
            "national_id_image",
            "issuance_date",
            "medical_center",
        ]


class VeterinarianSerializer(serializers.ModelSerializer):
    """Veterinarian Serializer"""

    class Meta:
        model = Veterinarian
        fields = "__all__"


class MedicalCenterSerializer(serializers.ModelSerializer):
    """Medical Center Serializer"""

    class Meta:
        model = MedicalCenter
        fields = "__all__"
