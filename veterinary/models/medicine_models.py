import os
from uuid import uuid4
from django.db import models

from common.models import BaseModel


def request_image_file_path(instance, filename):
    """Generate file path for request image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "medicine", "images", filename)


class Medicine(BaseModel):
    """Medicine Model"""

    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=request_image_file_path)
    analysis_result = models.TextField(
        null=True, blank=True
    )  # New field to store AI result

    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="medicines"
    )

    def __str__(self):
        return self.name if self.name else f"Medicine {self.id}"
