from rest_framework import serializers

from ..models import Veterinarian, MedicalCenter


class RegisterVeterinarianSerializer(serializers.ModelSerializer):
    """Register Veterinarian Serializer"""

    # Address Field
    street = serializers.CharField(write_only=True, required=True)
    clinic_name = serializers.CharField(write_only=True, required=False)
    latitude = serializers.CharField(write_only=True, required=False)
    longitude = serializers.CharField(write_only=True, required=False)

    # User Field
    fullName = serializers.CharField(write_only=True, required=False)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Veterinarian
        fields = [
            "medical_license",
            "license_type",
            "license_image",
            "national_id_image",
            "issuance_date",
            "medical_center",
            "slug",
            # Address Field
            "province",
            "city",
            "street",
            "clinic_name",
            "latitude",
            "longitude",
            # User Field
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
