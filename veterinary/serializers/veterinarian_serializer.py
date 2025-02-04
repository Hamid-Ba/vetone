from rest_framework import serializers

from ..models import Veterinarian


class RegisterVeterinarianSerializer(serializers.ModelSerializer):
    """Register Veterinarian Serializer"""

    class Meta:
        model = Veterinarian
        fields = [
            "medical_license",
            "license_image",
            "national_id_image",
            "issuance_date",
            "medical_center",
        ]
