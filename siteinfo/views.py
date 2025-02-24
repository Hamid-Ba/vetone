# TODO Add About Us Stats
from rest_framework import views, permissions, response, status


class AboutUsStatsAPI(views.APIView):
    """About Us Stats API"""

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        res = {"veterinarians": 100, "ranchers": 100, "centers": 100, "requests": 100}

        return response.Response({"response": res}, status=status.HTTP_200_OK)
