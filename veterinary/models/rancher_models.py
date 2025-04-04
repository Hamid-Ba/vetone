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

    # Favorite vets (this is for favorites only)
    favorite_veterinarians = models.ManyToManyField(
        "veterinary.Veterinarian",
        through="veterinary.FavoriteVeterinarian",
        related_name="favorited_by",
        blank=True,
    )

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

    def add_favorite(self, veterinarian):
        """Add a veterinarian to the favorites list."""
        if not FavoriteVeterinarian.objects.filter(
            rancher=self, veterinarian=veterinarian
        ).exists():
            FavoriteVeterinarian.objects.create(rancher=self, veterinarian=veterinarian)
            return True
        return False

    def remove_favorite(self, veterinarian):
        """Remove a veterinarian from the favorites list."""
        deleted, _ = FavoriteVeterinarian.objects.filter(
            rancher=self, veterinarian=veterinarian
        ).delete()
        return deleted > 0

    def get_favorites(self):
        """Retrieve all favorited veterinarians."""
        return self.favorite_veterinarians.all()

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


class FavoriteVeterinarian(models.Model):
    rancher = models.ForeignKey("veterinary.Rancher", on_delete=models.CASCADE)
    veterinarian = models.ForeignKey(
        "veterinary.Veterinarian", on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when added

    class Meta:
        unique_together = ("rancher", "veterinarian")  # Prevent duplicates

    def __str__(self):
        return (
            f"{self.rancher.user.fullName} favorited {self.veterinarian.user.fullName}"
        )
