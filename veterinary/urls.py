from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "veterinary"

router = DefaultRouter()
router.register(r"requests", RequestAPI)

urlpatterns = [
    path("", include(router.urls)),
    path("request/", CreateRequestAPI.as_view(), name="create_request"),
    path(
        "register_veterinarian/",
        RegisterVeterinarianAPI.as_view(),
        name="register_veterinarian",
    ),
    path("me/", VeterinarianAPI.as_view(), name="veterinarian-me"),
    path("<str:slug>", GetVeterinarianAPI.as_view(), name="get-veterinarian"),
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
        "ranchers/",
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
