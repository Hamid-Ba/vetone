"""
Gallery Module Serializer
"""

from rest_framework import serializers
from django.conf import settings
from gallery import models


class GallerySerializer(serializers.ModelSerializer):
    """Gallery Serializer"""

    class Meta:
        """Meta Class"""

        model = models.Gallery
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["url"] = settings.BACK_URL + instance.image.url

        return rep


class MediaSerializer(serializers.ModelSerializer):
    """Media Serializer"""

    class Meta:
        """Meta Class"""

        model = models.Media
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["url"] = settings.BACK_URL + instance.file.url

        return rep
