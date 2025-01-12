from datetime import datetime

from django.utils.dateparse import parse_datetime
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import (
    BuyTransactionSerializer,
    SellTransactionSerializer,
    TransactionHistorySerializer,
)


class BuyGoldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BuyTransactionSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            transaction = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellGoldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SellTransactionSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            transaction = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user_id = self.request.query_params.get("user_id", None)

        if user_id:
            queryset = Transaction.objects.filter(user_id=user_id)
        else:
            queryset = Transaction.objects.filter(user=self.request.user)

        return queryset
