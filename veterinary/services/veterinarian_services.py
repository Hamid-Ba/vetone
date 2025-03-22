from django.db import transaction

from province.models import Address


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
