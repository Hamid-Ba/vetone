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


class UpdateVeterinarianSerializer(serializers.ModelSerializer):
    """Veterinarian Serializer"""

    fullName = serializers.CharField(source="user.fullName", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)
    image = serializers.ImageField(source="user.image", read_only=True)

    class Meta:
        model = Veterinarian
        fields = "__all__"
        read_only_fields = ["slug", "rate", "user"]


class VeterinarianSerializer(UpdateVeterinarianSerializer):
    """Update Veterinarian Serializer"""

    city = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    medical_center = serializers.SerializerMethodField()

    def get_city(self, obj):
        if obj.city:
            return obj.city.name
        return None

    def get_province(self, obj):
        if obj.province:
            return obj.province.name
        return None

    def get_medical_center(self, obj):
        if obj.medical_center:
            return obj.medical_center.title
        return None

    class Meta(UpdateVeterinarianSerializer.Meta):
        pass


class MedicalCenterSerializer(serializers.ModelSerializer):
    """Medical Center Serializer"""

    class Meta:
        model = MedicalCenter
        fields = "__all__"


class RateSerializer(serializers.ModelSerializer):
    """Rate Serializer"""

    rate = serializers.IntegerField()

    class Meta:
        model = Veterinarian
        fields = ["rate"]

    def validate_rate(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rate must be between 1 and 5.")
        return value
