from django.contrib import admin
from blog import models
from jalali_date.admin import (
    ModelAdminJalaliMixin,
)


class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title", "short_desc", "desc")


admin.site.register(models.Blog, BlogAdmin)
