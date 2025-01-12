from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        BUY = "buy", "Buy"
        SELL = "sell", "Sell"

    class TransactionStatus(models.TextChoices):
        COMPLETED = "completed", "Completed"
        PENDING = "pending", "Pending"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount_rial = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    gold_weight_gram = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_gram = models.DecimalField(
        max_digits=15, decimal_places=2
    )  # Snapshot of price
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.COMPLETED,
    )

    def __str__(self):
        return f"Transaction {self.id} ({self.type}) - User {self.user_id}"
