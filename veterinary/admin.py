from django.contrib import admin

from .models import *


class AnimalRequestInline(admin.TabularInline):
    model = AnimalRequest
    extra = 1


class AnimalAdminModel(admin.ModelAdmin):
    """Animal Admin Model"""

    list_display = ["id", "name"]
    list_display_links = ["id", "name"]

    search_fields = ["name"]
    inlines = [AnimalRequestInline]


class RancherAdminModel(admin.ModelAdmin):
    """Rancher Admin Model"""

    list_display = ["id", "user"]
    list_display_links = ["id", "user"]


class VeterinarianAdminModel(admin.ModelAdmin):
    """Veterinarian Admin Model"""

    list_display = ["id", "code", "user", "medical_license", "state", "is_active"]
    list_display_links = ["id", "medical_license", "user"]
    list_editable = ["is_active", "state"]


class MedicalCenterAdminModel(admin.ModelAdmin):
    """MedicalCenter Admin Model"""

    list_display = ["id", "title", "description", "is_active"]
    list_display_links = ["id", "title"]
    list_editable = ["is_active"]


class RequestAdminModel(admin.ModelAdmin):
    list_display = ("id", "rancher", "veterinarian", "type", "date", "time")
    list_filter = ("type", "date")
    search_fields = ("rancher__user__phone", "veterinarian__user__phone")
    ordering = ("-created_at",)
    inlines = [AnimalRequestInline]


admin.site.register(Animal, AnimalAdminModel)
admin.site.register(Request, RequestAdminModel)
admin.site.register(Rancher, RancherAdminModel)
admin.site.register(Veterinarian, VeterinarianAdminModel)
admin.site.register(MedicalCenter, MedicalCenterAdminModel)
