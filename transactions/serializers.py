from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

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

    def create(self, validated_data):
        user = self.context["request"].user

        amount_rial = validated_data["amount_rial"]

        gold_weight_gram = amount_rial / GOLD_PRICE_PER_GRAM

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

    def validate_gold_weight_grams(self, value):
        if value <= 0:
            raise serializers.ValidationError("Gold weight must be greater than zero.")
        return value

    def create(self, validated_data):

        user = self.context["request"].user

        gold_weight_gram = validated_data.get("gold_weight_gram")

        amount_rial = Decimal(gold_weight_gram) * GOLD_PRICE_PER_GRAM

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
