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
    path(
        "ranchers",
        RancherListAPI.as_view(),
        name="ranchers",
    ),
    path(
        "remove_rancher/<str:phone>",
        RemoveRancherAPI.as_view(),
        name="remove_rancher",
    ),
    path(
        "animals/",
        AnimalListAPI.as_view(),
        name="animals",
    ),
    path(
        "search_veterinarian/",
        SearchVeterinarianAPI.as_view(),
        name="search_veterinarian",
    ),
]
