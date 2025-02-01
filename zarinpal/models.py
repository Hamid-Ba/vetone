"""
Payment Models Module
"""
from django.db import models
from common.models import BaseModel


class Payment(BaseModel):
    """Payment Model"""

    class PaymentStatus(models.IntegerChoices):
        """Payment Status Enums"""

        PAYMENT_CREATED = 1, "Payment Created"
        PAYMENT_DONE = 2, "Payment Done"
        PAYMENT_CANCELLED = 3, "Payment Cancelled"

    pay_amount = models.DecimalField(decimal_places=3, default=0, max_digits=12)
    desc = models.CharField(max_length=125, null=True, blank=True)
    ref_id = models.CharField(max_length=50, null=True, blank=True)
    authority = models.CharField(max_length=50, null=True, blank=True)
    is_payed = models.BooleanField(default=False)
    payed_date = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.PAYMENT_CREATED
    )

    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="payments"
    )

    def __str__(self) -> str:
        return f"User : {self.user}"
