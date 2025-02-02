import os
from uuid import uuid4
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from gallery import models as gallery_models


# Create your models here.
def blog_image_file_path(instance, filename):
    """Generate file path for category image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "blogs", filename)


class Blog(BaseModel):
    """Blog Model"""

    title = models.CharField(
        max_length=85, blank=False, null=False, verbose_name="عنوان"
    )
    slug = models.SlugField(
        max_length=170, blank=False, null=False, verbose_name="اسلاگ"
    )
    short_desc = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="توضیحات کوتاه"
    )
    desc = RichTextField(blank=True, null=True, verbose_name="توضیحات")

    image_alt = models.CharField(max_length=72, blank=True, null=True)
    image_title = models.CharField(max_length=125, blank=True, null=True)

    image = models.ForeignKey(
        gallery_models.Gallery,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="blogs",
        verbose_name="تصویر",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("مقاله")
        verbose_name_plural = _("مقالات")
