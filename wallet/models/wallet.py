from decimal import Decimal

from django.db import models

from common.models import BaseModel
from monitoring.models.observability import CodeLog


class Wallet(BaseModel):
    """Wallet Model"""

    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )  # Amount in Toman

    user = models.OneToOneField(
        "account.User", on_delete=models.CASCADE, related_name="wallet"
    )

    def charge(self, amount):
        """Charge the wallet by adding balance."""
        self.balance += amount
        self.save()

        # Create a transaction log
        Transaction.objects.create(
            wallet=self, amount=amount, description="Wallet charged", type="C"
        )

    def deduct(self, amount, description=None):
        """Deduct the specified amount if balance is sufficient."""
        # if self.balance >= amount:
        self.balance -= Decimal(str(amount))

        self.save()

        if self.balance <= 30000:
            # Sending a warning is not enough.

            pass
        if self.balance < 0:
            # Sending a notification is not enough and disable store
            CodeLog.log_client(
                "wallet.py", "def deduct", "your balance is under 0", None, self.user
            )

        # Create a transaction log for deduction
        if not description:
            description = "Wallet deduction for API call"

        Transaction.objects.create(
            wallet=self, amount=-amount, description=description, type="D"
        )
        # return True

        # return False  # Insufficient balance

    def __str__(self):
        return f"Wallet of {self.user.phone} : {self.balance} Toman"


class Transaction(BaseModel):
    """Transaction Log Model"""

    class TransactionType(models.TextChoices):
        charge = "C", "واریز"
        deduction = "D", "برداشت"

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(
        max_length=20, choices=TransactionType.choices, default=TransactionType.charge
    )  # Type of transaction
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Transaction of {self.amount} Toman on {self.date}"
