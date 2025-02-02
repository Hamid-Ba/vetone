from django.contrib import admin

from province.models import Province, City, Address

# Register your models here.


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "province"]
    list_display_links = ["id", "name"]
    list_filter = ["province"]
    search_fields = ["name", "province__name"]


class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "city", "user", "street"]
    list_display_links = ["id", "city", "user"]
    list_filter = ["city"]
    search_fields = ["street", "user__phone"]


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)
