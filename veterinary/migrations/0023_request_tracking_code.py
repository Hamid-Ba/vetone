# Generated by Django 4.2.20 on 2025-03-29 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("veterinary", "0022_remove_animalrequest_sign_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="tracking_code",
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
