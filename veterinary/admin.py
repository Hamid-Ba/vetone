from django.contrib import admin

from .models import *


class VeterinarianAdminModel(admin.ModelAdmin):
    """Veterinarian Admin Model"""

    list_display = ["id", "user", "medical_license", "is_active"]
    list_display_links = ["id", "medical_license", "user"]
    list_editable = ["is_active"]


admin.site.register(Veterinarian, VeterinarianAdminModel)
