from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from wallet.models import Wallet

from .constants import GOLD_PRICE_PER_GRAM
from .models import Transaction

User = get_user_model()


class BuyTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "amount_rial",
            "gold_weight_gram",
            "price_per_gram",
            "status",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "price_per_gram": {"read_only": True},
            "gold_weight_gram": {"read_only": True},
        }

    def validate_amount_rial(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        """Check if the user has enough balance in their wallet."""
        user = self.context["request"].user
        wallet = getattr(user, "wallet", None)

        if wallet is None:
            raise ValidationError("Wallet does not exist for the user.")

        amount_rial = data["amount_rial"]
        if wallet.balance_rial < amount_rial:
            raise ValidationError("Insufficient wallet balance to make this purchase.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        wallet = user.wallet

        amount_rial = validated_data["amount_rial"]

        gold_weight_gram = amount_rial / GOLD_PRICE_PER_GRAM

        with transaction.atomic():
            # Update wallet balances
            wallet.balance_rial -= amount_rial
            wallet.balance_gram += gold_weight_gram
            wallet.save()

            # Create the transaction
            transaction = Transaction.objects.create(
                user=user,
                type=Transaction.TransactionType.BUY,
                amount_rial=amount_rial,
                gold_weight_gram=gold_weight_gram,
                price_per_gram=GOLD_PRICE_PER_GRAM,
                status=Transaction.TransactionStatus.COMPLETED,
            )

        return transaction


class SellTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "amount_rial",
            "gold_weight_gram",
            "price_per_gram",
            "status",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "price_per_gram": {"read_only": True},
            "amount_rial": {"read_only": True},
        }

    def validate_gold_weight_gram(self, value):
        if value <= 0:
            raise serializers.ValidationError("Gold weight must be greater than zero.")
        return value

    def validate(self, data):
        """Check that the user has enough gold in their wallet."""
        user = self.context["request"].user
        wallet = getattr(user, "wallet", None)

        if wallet is None:
            raise ValidationError("Wallet does not exist for the user.")

        gold_weight_gram = data["gold_weight_gram"]

        if wallet.balance_gram < gold_weight_gram:
            raise ValidationError(
                "Insufficient gold balance in wallet to complete the sale."
            )

        return data

    def create(self, validated_data):

        user = self.context["request"].user
        wallet = user.wallet

        gold_weight_gram = validated_data.get("gold_weight_gram")

        amount_rial = Decimal(gold_weight_gram) * GOLD_PRICE_PER_GRAM

        with transaction.atomic():
            # Deduct the amount from the wallet
            wallet.balance_rial += amount_rial
            wallet.balance_gram -= gold_weight_gram
            wallet.save()

            # Create the transaction
            transaction = Transaction.objects.create(
                user=user,
                type=Transaction.TransactionType.SELL,
                gold_weight_gram=gold_weight_gram,
                amount_rial=amount_rial,
                price_per_gram=GOLD_PRICE_PER_GRAM,
                status=Transaction.TransactionStatus.COMPLETED,
            )

        return transaction


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "type",
            "amount_rial",
            "gold_weight_gram",
            "price_per_gram",
            "status",
            "date",
        ]
