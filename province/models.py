"""
Province Module Models
"""
from django.db import models
from django.shortcuts import reverse

from common.models import BaseModel


class Province(models.Model):
    """Province Model"""

    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=125, blank=False, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cafe:cafes_by_province", kwargs={"province_slug": self.slug})


class City(models.Model):
    """City Model"""

    name = models.CharField(max_length=85, blank=False, null=False)
    slug = models.SlugField(max_length=225, blank=False, null=False)
    province = models.ForeignKey(
        Province, null=False, blank=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Address(BaseModel):
    """Address Model"""

    street = models.CharField(
        max_length=255, blank=False, null=False, default="لطفا پر کنید"
    )
    city = models.ForeignKey(City, null=False, blank=False, on_delete=models.CASCADE)

    # veterinarain info
    clinic_name = models.CharField(max_length=255, blank=True, null=True)
    google_map_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    )

    # rancher info
    fullName = models.CharField(max_length=255, blank=True, null=True)
    village_name = models.CharField(max_length=255, blank=True, null=True)

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="addresses",
    )

    def __str__(self):
        return f"{self.user.phone} - {self.city.name} - {self.street}"

    class Meta:
        verbose_name_plural = "Addresses"
