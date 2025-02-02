"""
Province Module Serializers
"""
from rest_framework import serializers

from province.models import Province, City, Address


class ProvinceSerializer(serializers.ModelSerializer):
    """Province Serializer"""

    class Meta:
        """Meta Class"""

        model = Province
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    """City Serializer"""

    class Meta:
        """Meta Class"""

        model = City
        fields = ["id", "name"]


class AddressSerializer(serializers.ModelSerializer):
    """Address Serializer"""

    city = CitySerializer(many=False)

    class Meta:
        """Meta Class"""

        model = Address
        fields = "__all__"
        read_only_fields = ["user"]
