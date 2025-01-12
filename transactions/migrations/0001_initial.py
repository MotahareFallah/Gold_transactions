# Generated by Django 5.1.4 on 2025-01-12 06:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("buy", "Buy"), ("sell", "Sell")], max_length=10
                    ),
                ),
                (
                    "amount_rial",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "gold_weight_gram",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "price_per_gram",
                    models.DecimalField(decimal_places=2, max_digits=15),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("completed", "Completed"),
                            ("pending", "Pending"),
                            ("failed", "Failed"),
                        ],
                        default="completed",
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
