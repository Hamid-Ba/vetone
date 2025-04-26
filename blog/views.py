"""
Blog Module Views
"""
from django.utils import timezone
from rest_framework import generics, filters

from config import pagination
from blog import serializers, models


class BlogDetailView(generics.RetrieveAPIView):
    """Detail Of Blog View"""

    lookup_field = "slug"
    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogSerializer


class BlogsView(generics.ListAPIView):
    """List Of Blogs View"""

    queryset = models.Blog.objects.all()
    # pagination_class = pagination.StandardPagination
    serializer_class = serializers.BlogSerializer

    def get_queryset(self):
        return self.queryset.order_by("-id")


class LatestBlogsView(generics.ListAPIView):
    """List Of Latest Blogs View"""

    queryset = models.Blog.objects.order_by("-id")
    serializer_class = serializers.LatestBlogSerializer

    def get_queryset(self):
        return self.queryset[:3]


class SearchBlogsAPI(generics.ListAPIView):
    """Search Blogs API"""

    queryset = models.Blog.objects.all()
    serializer_class = serializers.BlogSerializer
    # pagination_class = pagination.StandardPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title", "slug", "short_desc"]

    def get_queryset(self):
        return self.queryset.order_by("-id")
