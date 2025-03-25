from django.core.exceptions import ObjectDoesNotExist


from django.db.models.signals import post_save
from django.dispatch import receiver

from monitoring.models.observability import CodeLog
from notifications import KavenegarSMS
from veterinary.models import Veterinarian, Rancher


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
    if instance.state == "C":
        sender.objects.fill_unique_code(instance.id)

    if instance.state == "R" and not instance.code:
        kavenegar = KavenegarSMS()
        kavenegar.reject(instance.user.phone)
        kavenegar.send()
