from rest_framework import serializers

from ..models import Animal, Rancher


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
