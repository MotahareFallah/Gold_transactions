from django.contrib import admin
from .models import Wallet

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_gram', 'balance_rial')

admin.site.register(Wallet, WalletAdmin)
