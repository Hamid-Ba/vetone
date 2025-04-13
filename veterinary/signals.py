from django.core.exceptions import ObjectDoesNotExist


from django.db.models.signals import post_save
from django.dispatch import receiver

from monitoring.models.observability import CodeLog
from notifications import KavenegarSMS
from veterinary.models import Veterinarian, Rancher, Request
from .tasks.request_tasks import *


@receiver(post_save, sender=Veterinarian, dispatch_uid="veterinarian_register")
def after_veterinarian_registration(sender, instance, created, **kwargs):
    """Delete Rancher Account Of Registrated Veterinarian"""
    if created:
        try:
            rancher = Rancher.objects.get(user=instance.user)
            rancher.delete()
        except ObjectDoesNotExist as e:
            CodeLog.log_warning(
                "signals.py",
                "def after_veterinarian_registration",
                "Rancher Does Not Found",
                {"user_phone": instance.user.phone},
            )
            pass


@receiver(post_save, sender=Veterinarian, dispatch_uid="fille_unique_code")
def fill_veterinarian_unique_code(sender, instance, created, **kwargs):
    """Fill Veterinarian Unique Code After Confirmed"""
    if not created:
        if instance.state == "C":
            sender.objects.fill_unique_code(instance.id)

        if instance.state == "R" and not instance.code:
            kavenegar = KavenegarSMS()
            kavenegar.reject(instance.user.phone, instance.user.phone)
            kavenegar.send()


@receiver(post_save, sender=Request, dispatch_uid="notify_created_request")
def notify_veterinarian_and_rancher(sender, instance, created, **kwargs):
    """Fill Veterinarian Unique Code After Confirmed"""

    if created:
        veter_phone = instance.veterinarian.user.phone
        rancher_phone = instance.rancher.user.phone

        inform_rancher_for_new_request.delay(rancher_phone, instance.tracking_code)
        inform_veterinarian_for_new_request.delay(veter_phone, instance.tracking_code)


@receiver(post_save, sender=Request, dispatch_uid="notify_request_state")
def notify_rancher_for_request_state(sender, instance, created, **kwargs):
    """Fill Veterinarian Unique Code After Confirmed"""
    if not created:
        rancher_phone = instance.rancher.user.phone
        if instance.state == "C":
            inform_rancher_for_confirm_or_reject_request.delay(
                rancher_phone, instance.tracking_code, True
            )
        elif instance.state == "R":
            inform_rancher_for_confirm_or_reject_request.delay(
                rancher_phone, instance.tracking_code, False
            )
        elif instance.state == "D":
            inform_rancher_for_end_of_request.delay(
                rancher_phone, instance.tracking_code
            )