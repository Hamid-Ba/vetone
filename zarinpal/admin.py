from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    """Payment admin"""

    list_display = [
        "user",
        "pay_amount",
        "ref_id",
        "is_payed",
        "status",
        "payed_date",
        "created_at",
    ]
    list_display_links = ["user", "pay_amount", "created_at"]
    list_editable = (
        "payed_date",
        "status",
        "is_payed",
    )


admin.site.register(Payment, PaymentAdmin)
