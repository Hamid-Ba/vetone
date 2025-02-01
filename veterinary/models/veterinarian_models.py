import os
from uuid import uuid4
from django.db import models

from common.models import BaseModel


def veterinarian_image_file_path(instance, filename):
    """Generate file path for Veterinarian image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "veterinarian", filename)


class Veterinarian(BaseModel):
    medical_license = models.CharField(max_length=72, null=False, blank=False)
    license_image = models.ImageField(
        null=False, blank=False, upload_to=veterinarian_image_file_path
    )
    national_id_image = models.ImageField(
        null=False, blank=False, upload_to=veterinarian_image_file_path
    )
    issuance_date = models.DateField(null=False, blank=False)

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="veterinarian",
    )

    city = models.ForeignKey(
        "province.City",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="veterinarians",
    )

    def __str__(self):
        return f"{self.medical_license} - {self.user.phone}"
