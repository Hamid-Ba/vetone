from django.contrib import admin
from .models import *


class WalletAdmin(admin.ModelAdmin):
    """Admin interface for Wallet"""

    list_display = ("id", "user", "balance")
    list_filter = ("user",)


class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction"""

    list_display = ("wallet", "amount", "type", "description", "date")
    search_fields = ("wallet__user__phone", "wallet__user__fullName")
    list_filter = ("date", "type")
    readonly_fields = ("wallet", "amount", "description", "date")


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
