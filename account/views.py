"""
Account Module Views
"""
from rest_framework import generics, permissions, authentication, views
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout


from rest_framework.response import Response
from account.serializers import (
    AuthenticationSerializer,
    AuthTokenSerializer,
    UserSerializer,
)


class LoginOrRegisterView(generics.CreateAPIView):
    """Login Or Register View"""

    serializer_class = AuthenticationSerializer


class LogoutView(views.APIView):
    """Logout View"""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        """Logout Action"""
        try:
            request.user.auth_token.delete()
        except:
            None
        logout(request)
        return Response({"detail": "شما با موفقیت خارج شدید"})


class AuthTokenView(ObtainAuthToken):
    """Auth Token View For Create Valid Token"""

    serializer_class = AuthTokenSerializer


class UserView(generics.RetrieveUpdateAPIView):
    """Retrieve Or Update APIView for User"""

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """Retrieve The Authorized User"""
        return self.request.user
