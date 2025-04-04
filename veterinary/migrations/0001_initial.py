# Generated by Django 4.2.18 on 2025-02-01 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import veterinary.models.veterinarian_models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Veterinarian",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("medical_license", models.CharField(max_length=72)),
                (
                    "license_image",
                    models.ImageField(
                        upload_to=veterinary.models.veterinarian_models.veterinarian_image_file_path
                    ),
                ),
                (
                    "national_id_image",
                    models.ImageField(
                        upload_to=veterinary.models.veterinarian_models.veterinarian_image_file_path
                    ),
                ),
                ("issuance_date", models.DateField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="veterinarian",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
