from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

from monitoring.models.observability import CodeLog
from notifications import KavenegarSMS
from wallet.models.wallet import Wallet
from veterinary.models import Rancher

from .models import User
from decouple import config


@receiver(post_save, sender=User, dispatch_uid="user_register")
def after_user_registration(sender, instance, created, **kwargs):
    """Create Wallet For User after Registration"""
    IS_TEST = config("IS_TEST", default=False, cast=bool)
    if created:
        Wallet.objects.get_or_create(user=instance, balance=50000)
        if not instance.is_staff:
            Rancher.objects.get_or_create(user=instance)
    if not IS_TEST:
        if created:
            if not instance.is_staff:
                sms = KavenegarSMS()

                phone_support = settings.PHONE_SUPPORT

                try:
                    sms.notify_welcomeNewUser(
                        receptor=instance.phone, token=phone_support
                    )
                    sms.send()
                except Exception as e:
                    CodeLog.log_critical(
                        "signals.py",
                        "def after_user_registration",
                        str(e),
                        {"phone": instance.phone, "line": 30},
                    )

                admins = User.objects.get_admins()
                try:
                    for admin in admins:
                        sms.notify_NewUser_for_admins(
                            receptor=admin.phone, token=instance.phone
                        )
                        sms.send()
                except Exception as e:
                    CodeLog.log_critical(
                        "signals.py",
                        "def after_user_registration",
                        str(e),
                        {"phone": instance.phone, "line": 45},
                    )
