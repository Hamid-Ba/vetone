from rest_framework import generics, viewsets, permissions, authentication, mixins
from rest_framework.parsers import JSONParser, MultiPartParser

from config.pagination import StandardPagination
from ..models import Request
from ..serializers import RequestSerializer, CreateRequestSerializer
import json


class CreateRequestAPI(generics.CreateAPIView):
    """Create Request API"""

    queryset = Request.objects.all()
    serializer_class = CreateRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(rancher=self.request.user.rancher)


class RequestAPI(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """List, Get, Update, Destroy Request API"""

    queryset = Request.objects.order_by("-id")
    serializer_class = RequestSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        try:
            return self.queryset.filter(rancher=self.request.user.rancher)
        except:
            return self.queryset.filter(veterinarian=self.request.user.veterinarian)
