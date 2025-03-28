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

    veterinarians = models.ManyToManyField(
        "veterinary.Veterinarian", blank=True, related_name="ranchers"
    )

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="rancher",
    )

    def __str__(self):
        return f"{self.user.fullName} - {self.user.phone}"


class Animal(BaseModel):
    """Animal Model"""

    name = models.CharField(max_length=125, blank=False, null=False)
    image = models.ForeignKey(
        "gallery.Gallery",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="animals",
    )

    def __str__(self):
        return self.name
