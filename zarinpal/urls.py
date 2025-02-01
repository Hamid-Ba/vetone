from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)
from . import views

router = DefaultRouter()
router.register("store", views.PaymentsView)

app_name = "payment"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "make_transaction/", views.TransactionRequest.as_view(), name="make_transaction"
    ),
    path(
        "verify_transaction/",
        views.TransactionVerify.as_view(),
        name="verify_transaction",
    ),
]
