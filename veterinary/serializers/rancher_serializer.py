from rest_framework import serializers

from ..models import Rancher


class RancherSerializer(serializers.ModelSerializer):
    """Rancher Serializer"""

    class Meta:
        model = Rancher
        fields = "__all__"
