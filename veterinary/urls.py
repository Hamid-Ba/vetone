from django.urls import path

from .views import *

app_name = "veterinary"


urlpatterns = [
    path(
        "register_veterinarian/",
        RegisterVeterinarianAPI.as_view(),
        name="register_veterinarian",
    ),
    path(
        "centers/",
        MedicalCenterListAPI.as_view(),
        name="centers",
    ),
    path(
        "add_rancher/",
        AddRancherAPI.as_view(),
        name="add_rancher",
    ),
]
