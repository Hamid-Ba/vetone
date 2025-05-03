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
        "remove_rancher/<str:phone>/",
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
    # path("favorites/", FavoriteVeterinarianListView.as_view(), name="favorite-list"),
    path("favorites/add/", AddFavoriteVeterinarianView.as_view(), name="add-favorite"),
    path(
        "favorites/", FavoriteVeterinariansView.as_view(), name="favorite-veterinarians"
    ),
    path(
        "favorites/remove/<int:veterinarian_id>/",
        RemoveFavoriteVeterinarianView.as_view(),
        name="remove-favorite",
    ),
    path(
        "rate/<int:request_id>/",
        RateAPI.as_view(),
        name="rate",
    ),
    path("medicines/", MedicineListView.as_view(), name="medicine-list"),
    path("medicines/<int:pk>/", MedicineDetailView.as_view(), name="medicine-detail"),
    path("medicines/create/", MedicineCreateView.as_view(), name="medicine-create"),
    path("<str:slug>/", GetVeterinarianAPI.as_view(), name="get-veterinarian"),
]
