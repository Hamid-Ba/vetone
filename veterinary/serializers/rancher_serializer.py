from rest_framework import serializers

from ..models import Animal, Rancher, Veterinarian, FavoriteVeterinarian


class AnimalSerializer(serializers.ModelSerializer):
    """Animal Serializer"""

    class Meta:
        model = Animal
        fields = "__all__"


class RancherSerializer(serializers.ModelSerializer):
    """Rancher Serializer"""

    class Meta:
        model = Rancher
        fields = "__all__"


class RancherVeterinarianSerializer(serializers.Serializer):
    """Rancher Veterinarian Serializer"""

    image = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    fullName = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    def get_image(self, obj):
        try:
            return obj.user.image.path
        except:
            return None

    def get_phone(self, obj):
        return obj.user.phone

    def get_address(self, obj):
        address = obj.user.addresses.first()

        if address:
            return f"{address.latitude} - {address.longitude}"
        else:
            return None

    def get_latitude(self, obj):
        address = obj.user.addresses.first()

        if address:
            return f"{address.latitude}"
        else:
            return None

    def get_longitude(self, obj):
        address = obj.user.addresses.first()

        if address:
            return f"{address.longitude}"
        else:
            return None

    def get_fullName(self, obj):
        return obj.user.fullName

    class Meta:
        fields = ["image", "phone", "fullName", "address", "latitude", "longitude"]


class VeterinarianSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="user.fullName", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)
    image = serializers.ImageField(source="user.image", read_only=True)

    class Meta:
        model = Veterinarian
        fields = "__all__"  # Adjust this if you want to exclude some fields


class FavoriteVeterinarianSerializer(serializers.ModelSerializer):
    veterinarian_id = serializers.PrimaryKeyRelatedField(
        queryset=Veterinarian.objects.all(), source="veterinarian", write_only=True
    )

    class Meta:
        model = FavoriteVeterinarian
        fields = ["id", "veterinarian_id", "added_at"]

    def create(self, validated_data):
        """Add a veterinarian to the rancher's favorite list"""
        rancher = self.context["request"].user.rancher  # Assuming user is a rancher
        veterinarian = validated_data["veterinarian"]
        favorite, created = FavoriteVeterinarian.objects.get_or_create(
            rancher=rancher, veterinarian=veterinarian
        )
        if not created:
            raise serializers.ValidationError(
                "This veterinarian is already in favorites."
            )
        return favorite
