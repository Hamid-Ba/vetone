import os
from uuid import uuid4
from django.db import models

from common.models import BaseModel
from notifications import KavenegarSMS


def veterinarian_image_file_path(instance, filename):
    """Generate file path for Veterinarian image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "veterinarian", filename)


class MedicalCenter(BaseModel):
    """Medical Center"""

    title = models.CharField(max_length=72, null=False, blank=False)
    description = models.CharField(max_length=225, null=True, blank=True)

    gallery = models.ForeignKey(
        "gallery.Gallery",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="centers",
    )

    def __str__(self):
        return self.title


class VeterinarianManager(models.Manager):
    """Veterinarian Manager"""

    def get_confirmed_veters(self):
        """Returns a list of Veterinarian that have been confirmed"""
        return self.filter(state="C", is_active=True).values()

    def fill_unique_code(self, veterinarian_id):
        """Change Veterinarian State to Confirmed"""
        veterinarian = self.filter(id=veterinarian_id).get()
        if veterinarian.state == "C":
            if not veterinarian.code:
                veterinarian.code = str(10000 + veterinarian_id)
                # veterinarian.charge_veterinarian(days=31, is_first=True)
                veterinarian.save()

                IS_TEST = os.getenv("IS_TEST", default=False)
                if not IS_TEST:
                    # Send Confirm SMS
                    kavenegar = KavenegarSMS()
                    kavenegar.confirm(veterinarian.user.phone, veterinarian.code)
                    kavenegar.send()

        return veterinarian


class Veterinarian(BaseModel):
    class WorkStatus(models.TextChoices):
        Busy = "B", "Busy"
        Examination = "E", "Examination"
        Free = "F", "Free"
        Responsible = "R", "Responsible"

    class LicenseType(models.TextChoices):
        Test1 = "1", "Test1"
        Test2 = "2", "Test2"

    class VeterinarianState(models.TextChoices):
        PENDING = "P", "Pending"
        CONFIRMED = "C", "Confirmed"
        REJECTED = "R", "Rejected"

    slug = models.SlugField(null=False, blank=False)
    clinic_name = models.CharField(max_length=225, null=False, blank=False)
    medical_license = models.CharField(max_length=72, null=False, blank=False)
    license_type = models.CharField(
        max_length=1, default=LicenseType.Test1, choices=LicenseType.choices
    )
    license_image = models.ImageField(
        null=False, blank=False, upload_to=veterinarian_image_file_path
    )
    national_id_image = models.ImageField(
        null=False, blank=False, upload_to=veterinarian_image_file_path
    )
    issuance_date = models.DateField(null=False, blank=False)

    bio = models.CharField(max_length=1000, null=True, blank=True)

    state = models.CharField(
        max_length=1, default=WorkStatus.Busy, choices=WorkStatus.choices
    )

    background_image = models.ImageField(
        null=True, blank=True, upload_to=veterinarian_image_file_path
    )

    rate = models.IntegerField(default=0)
    surgery = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)

    code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    state = models.CharField(
        max_length=1,
        default=VeterinarianState.PENDING,
        choices=VeterinarianState.choices,
    )

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="veterinarian",
    )

    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.CASCADE, null=False, blank=False
    )

    province = models.ForeignKey(
        "province.Province",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="veterinarians",
    )

    city = models.ForeignKey(
        "province.City",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="veterinarians",
    )

    objects = VeterinarianManager()

    def __str__(self):
        return f"{self.medical_license} - {self.user.phone}"
