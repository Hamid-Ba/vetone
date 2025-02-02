from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)

from . import views


router = DefaultRouter()
router.register("addresses", views.AddressViewSet)

app_name = "province"

urlpatterns = [
    path("", include(router.urls)),
    path("addresses", views.AddressListAPI.as_view(), name="addresses"),
]
