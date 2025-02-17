from django.contrib import admin

from .models import *


class AnimalAdminModel(admin.ModelAdmin):
    """Animal Admin Model"""

    list_display = ["id", "name"]
    list_display_links = ["id", "name"]

    search_fields = ["name"]


class RancherAdminModel(admin.ModelAdmin):
    """Rancher Admin Model"""

    list_display = ["id", "user"]
    list_display_links = ["id", "user"]


class VeterinarianAdminModel(admin.ModelAdmin):
    """Veterinarian Admin Model"""

    list_display = ["id", "user", "medical_license", "is_active"]
    list_display_links = ["id", "medical_license", "user"]
    list_editable = ["is_active"]


class MedicalCenterAdminModel(admin.ModelAdmin):
    """MedicalCenter Admin Model"""

    list_display = ["id", "title", "description", "is_active"]
    list_display_links = ["id", "title"]
    list_editable = ["is_active"]


admin.site.register(Animal, AnimalAdminModel)
admin.site.register(Rancher, RancherAdminModel)
admin.site.register(Veterinarian, VeterinarianAdminModel)
admin.site.register(MedicalCenter, MedicalCenterAdminModel)
