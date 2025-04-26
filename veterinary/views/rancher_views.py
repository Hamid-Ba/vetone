from rest_framework import (
    views,
    status,
    generics,
    response,
    permissions,
    authentication,
)
from drf_spectacular.utils import extend_schema

from config.pagination import StandardPagination


from ..models import Animal, FavoriteVeterinarian
from ..serializers import rancher_serializer


class AnimalListAPI(generics.ListAPIView):
    """Animal List API"""

    queryset = Animal.objects.all()
    serializer_class = rancher_serializer.AnimalSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    # pagination_class = StandardPagination


class FavoriteVeterinarianListView(generics.ListAPIView):
    """List all favorite veterinarians of the logged-in rancher"""

    serializer_class = rancher_serializer.FavoriteVeterinarianSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return FavoriteVeterinarian.objects.filter(rancher=self.request.user.rancher)


class AddFavoriteVeterinarianView(generics.CreateAPIView):
    """Add a veterinarian to favorites"""

    serializer_class = rancher_serializer.FavoriteVeterinarianSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


class RemoveFavoriteVeterinarianView(views.APIView):
    """Remove a veterinarian from the favorites list"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def delete(self, request, veterinarian_id):
        rancher = request.user.rancher
        try:
            favorite = FavoriteVeterinarian.objects.get(
                rancher=rancher, veterinarian_id=veterinarian_id
            )
            favorite.delete()
            return response.Response(
                {"message": "Removed from favorites."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except FavoriteVeterinarian.DoesNotExist:
            return response.Response(
                {"error": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND
            )


class FavoriteVeterinariansView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    @extend_schema(responses=rancher_serializer.VeterinarianSerializer(many=True))
    def get(self, request):
        # Get the rancher of the logged-in user
        rancher = request.user.rancher

        # Get all favorite veterinarians
        favorite_vets = rancher.favorite_veterinarians.all()

        # Serialize the data
        serializer = rancher_serializer.VeterinarianSerializer(favorite_vets, many=True)

        return response.Response(serializer.data)
