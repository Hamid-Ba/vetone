from rest_framework import (
    generics,
    permissions,
    authentication,
)

from config.pagination import StandardPagination


from ..models import Animal
from ..serializers import rancher_serializer


class AnimalListAPI(generics.ListAPIView):
    """Animal List API"""

    queryset = Animal.objects.all()
    serializer_class = rancher_serializer.AnimalSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = StandardPagination
