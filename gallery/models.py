import os
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

# Create your models here.


def gallery_image_file_path(instance, filename):
    """Generate file path for image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "gallery", filename)


def medial_video_file_path(instance, filename):
    """Generate file path for media"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "media", filename)


class Gallery(models.Model):
    """Gallery model"""

    title = models.CharField(
        max_length=125, blank=True, null=True, verbose_name="عنوان"
    )
    image = models.ImageField(
        null=False, upload_to=gallery_image_file_path, verbose_name="تصویر"
    )

    is_show = models.BooleanField(default=False, verbose_name="قابل نمایش در سایت")

    def __str__(self):
        if self.title:
            return self.title
        return self.image.name

    # class Meta:
    #     verbose_name = _("گالری")
    #     verbose_name_plural = _("گالری")


class Media(models.Model):
    """Media model"""

    title = models.CharField(
        max_length=125, blank=True, null=True, verbose_name="عنوان"
    )
    thumbnail = models.ImageField(
        null=True, blank=True, upload_to=gallery_image_file_path, verbose_name="تصویر"
    )
    file = models.FileField(
        null=False, upload_to=medial_video_file_path, verbose_name="فایل"
    )
    is_show = models.BooleanField(default=False, verbose_name="قابل نمایش در سایت")

    def __str__(self):
        if self.title:
            return self.title
        return self.file.name

    # class Meta:
    #     verbose_name = _("مدیا")
    #     verbose_name_plural = _("مدیا")
