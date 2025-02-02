"""
Blog Module Serializer
"""
from rest_framework import serializers

from blog import models
from gallery import serializers as gallery_serializers


class BlogSerializer(serializers.ModelSerializer):
    """Blog Serializer"""

    image = gallery_serializers.GallerySerializer(many=False)

    class Meta:
        model = models.Blog
        fields = "__all__"


class LatestBlogSerializer(serializers.ModelSerializer):
    """Latest Blog Serializer"""

    image = gallery_serializers.GallerySerializer(many=False)

    class Meta:
        model = models.Blog
        fields = ["title", "slug", "short_desc", "image"]
