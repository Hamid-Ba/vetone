from django.core.exceptions import ObjectDoesNotExist


from django.db.models.signals import post_save
from django.dispatch import receiver

from monitoring.models.observability import CodeLog
from veterinary.models import Veterinarian, Rancher


@receiver(post_save, sender=Veterinarian, dispatch_uid="veterinarian_register")
def after_veterinarian_registration(sender, instance, created, **kwargs):
    """Delete Rancher Account Of Registrated Veterinarian"""
    if created:
        try:
            rancher = Rancher.objects.get(user=instance.user)
            rancher.delete()
        except ObjectDoesNotExist as e:
            CodeLog.log_warning("signals.py", "def after_veterinarian_registration", "Rancher Does Not Found", {"user_phone": instance.user.phone})
            pass