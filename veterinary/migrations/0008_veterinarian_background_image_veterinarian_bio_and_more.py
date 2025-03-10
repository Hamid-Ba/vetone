# Generated by Django 4.2.18 on 2025-02-17 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import veterinary.models.rancher_models
import veterinary.models.veterinarian_models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("province", "0003_address_fullname"),
        ("veterinary", "0007_veterinarian_medical_center"),
    ]

    operations = [
        migrations.AddField(
            model_name="veterinarian",
            name="background_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=veterinary.models.veterinarian_models.veterinarian_image_file_path,
            ),
        ),
        migrations.AddField(
            model_name="veterinarian",
            name="bio",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="veterinarian",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=veterinary.models.veterinarian_models.veterinarian_image_file_path,
            ),
        ),
        migrations.AddField(
            model_name="veterinarian",
            name="license_type",
            field=models.CharField(
                choices=[("1", "Test1"), ("2", "Test2")], default="1", max_length=1
            ),
        ),
        migrations.CreateModel(
            name="Rancher",
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
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=veterinary.models.rancher_models.rancher_image_file_path,
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="ranchers",
                        to="province.city",
                    ),
                ),
                (
                    "province",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="ranchers",
                        to="province.province",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rancher",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
