from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment


@receiver(post_save, sender=Payment, dispatch_uid="charge_wallet")
def charge_wallet(sender, instance, created, **kwargs):
    """Charge Wallet If Payment Was Successful"""
    if not created:
        if instance.is_payed:
            wallet = instance.user.wallet
            wallet.charge(Decimal(instance.pay_amount))
