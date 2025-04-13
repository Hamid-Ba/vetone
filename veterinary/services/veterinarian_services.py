from django.db.models import Avg
from django.db import transaction

from province.models import Address
from ..models import Veterinarian, Request


@transaction.atomic
def add_veterinarian_address(*, user, street, clinic_name, latitude, longitude):
    """Add Rancher Service"""
    return Address.objects.create(
        user=user,
        street=street,
        clinic_name=clinic_name,
        latitude=latitude,
        longitude=longitude,
    )


def rate(*, veterinarian_id: int, rate: int):
    """Score Veterinarian"""

    veter = Veterinarian.objects.filter(id=veterinarian_id).first()

    if veter:
        mean_rate = Request.objects.filter(state="D", veterinarian=veter).aggregate(
            avg_rate=Avg("rate")
        )["avg_rate"]
        veter.rate = mean_rate
        veter.save()
        return True
    return False
