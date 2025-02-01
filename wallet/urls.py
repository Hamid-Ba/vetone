from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

app_name = "wallet"

urlpatterns = [
    path("", include(router.urls)),
    path("transactions", TransactionListAPI.as_view(), name="transactions"),
    path(
        "transaction/<int:id>/",
        TransactionDetailAPI.as_view(),
        name="transaction",
    ),
]
