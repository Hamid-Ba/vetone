from rest_framework import generics

from gallery import models, serializers


class GalleryList(generics.ListAPIView):
    queryset = models.Gallery.objects.filter(is_show=True).order_by("-id")
    serializer_class = serializers.GallerySerializer


class MediaList(generics.ListAPIView):
    queryset = models.Media.objects.filter(is_show=True).order_by("-id")
    serializer_class = serializers.MediaSerializer
