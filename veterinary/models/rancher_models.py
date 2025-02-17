import os
from uuid import uuid4
from django.db import models

from common.models import BaseModel


def rancher_image_file_path(instance, filename):
    """Generate file path for rancher image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "rancher", filename)


class Rancher(BaseModel):
    """Rancher Model"""
    image = models.ImageField(
        null=True, blank=True, upload_to=rancher_image_file_path
    )
           
    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="rancher",
    )

    province = models.ForeignKey(
        "province.Province",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="ranchers",
    )

    city = models.ForeignKey(
        "province.City",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="ranchers",
    )

    def __str__(self):
        return f"{self.user.fullName} - {self.user.phone}"
