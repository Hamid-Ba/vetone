from rest_framework import serializers

from ..models import Veterinarian, MedicalCenter


class RegisterVeterinarianSerializer(serializers.ModelSerializer):
    """Register Veterinarian Serializer"""

    fullName = serializers.CharField(
        write_only=True, required=False
    )  # To update User fullName
    image = serializers.ImageField(
        write_only=True, required=False
    )  # To update User image

    class Meta:
        model = Veterinarian
        fields = [
            "medical_license",
            "license_type",
            "license_image",
            "national_id_image",
            "issuance_date",
            "medical_center",
            "province",
            "city",
            "slug",
            "image",
            "fullName",
        ]

        read_only_fields = ["slug"]


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
