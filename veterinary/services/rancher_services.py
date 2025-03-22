from django.db import transaction

from ..models import Rancher, Veterinarian
from account.models import User
from province.models import Address


@transaction.atomic
def add_rancher(*, veterinarian_user, fullName, phone, latitude, longitude):
    """Add Rancher Service"""
    veterinarian = Veterinarian.objects.get(user=veterinarian_user)

    user, is_created = User.objects.get_or_create(phone=phone)
    user.fullName = fullName
    user.save()

    rancher = Rancher.objects.get(user=user)
    rancher.veterinarians.add(veterinarian)

    Address.objects.create(user=user, latitude=latitude, longitude=longitude)

    return rancher


def remove_rancher(*, veterinarian_user: User, rancher: Rancher):
    """Remove Rancher"""
    try:
        veterinarian = Veterinarian.objects.get(user=veterinarian_user)

        rancher.veterinarians.remove(veterinarian)
        rancher.save()
    except:
        return False

    return not rancher.veterinarians.contains(veterinarian)
