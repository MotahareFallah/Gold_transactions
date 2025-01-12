from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_gram = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_rial = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.user.username} - {self.balance_gram} grams / {self.balance_rial} Rial"

