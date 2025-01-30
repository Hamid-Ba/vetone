from django.urls import include, path
from rest_framework import routers

from .views import *

app_name = "veterinary"


urlpatterns = [
    path(
        "register_veterinarian/",
        RegisterVeterinarianAPI.as_view(),
        name="register_veterinarian",
    ),
]
