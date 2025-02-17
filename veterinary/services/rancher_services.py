from django.db import transaction

from ..models import Rancher, Veterinarian
from account.models import User
from province.models import Address


@transaction.atomic
def add_rancher(*, veterinarian_user, fullName, phone, village_name, city_id):
    """Add Rancher Service"""
    veterinarian = Veterinarian.objects.get(user=veterinarian_user)

    user, is_created = User.objects.get_or_create(phone=phone)
    user.fullName = fullName
    user.save()

    rancher = Rancher.objects.get(user=user)
    rancher.veterinarians.add(veterinarian)

    Address.objects.create(user=user, village_name=village_name, city_id=city_id)

    return rancher
