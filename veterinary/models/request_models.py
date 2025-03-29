import os
from uuid import uuid4
from django.db import models

from common.models import BaseModel


def request_image_file_path(instance, filename):
    """Generate file path for request image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "request", "images", filename)


def request_voice_file_path(instance, filename):
    """Generate file path for request voice"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "request", "voices", filename)


def request_video_file_path(instance, filename):
    """Generate file path for request video"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "request", "videos", filename)


class Request(BaseModel):
    """Rancher Model"""

    class RequestType(models.TextChoices):
        Tell = "T", "Tell"
        SMS = "S", "SMS"
        INPERSON = "IP", "In-Person"

    tracking_code = models.BigIntegerField()
    description = models.TextField(null=True, blank=True)
    voice = models.FileField(null=True, blank=True, upload_to=request_voice_file_path)
    video = models.FileField(null=True, blank=True, upload_to=request_video_file_path)
    type = models.CharField(
        max_length=2, default=RequestType.INPERSON, choices=RequestType.choices
    )
    date = models.DateField(blank=False, null=False)
    time = models.TimeField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to=request_image_file_path)

    rancher = models.ForeignKey(
        "veterinary.Rancher",
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name="requests",
    )

    veterinarian = models.ForeignKey(
        "veterinary.Veterinarian",
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name="requests",
    )

    def __str__(self):
        return f"Rancher: {self.rancher.user.phone} - Veteinarian: {self.veterinarian.user.phone} - {self.created_at}"


class AnimalRequest(BaseModel):
    """Animal Request Model"""

    count = models.PositiveIntegerField(default=1)

    animal = models.ForeignKey(
        "veterinary.Animal",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="requests",
    )
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="animals",
    )

    def __str__(self):
        return f"Request ID: {self.request.id} - {self.animal}"


# class RequestImage(BaseModel):
#     """Request Image Model"""

#     image = models.ImageField(
#         null=False, blank=False, upload_to=request_image_file_path
#     )
#     request = models.ForeignKey(
#         Request,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False,
#         related_name="images",
#     )
