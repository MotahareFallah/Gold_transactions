from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "type",
        "amount_rial",
        "gold_weight_gram",
        "price_per_gram",
        "status",
        "date",
    )


admin.site.register(Transaction, TransactionAdmin)
