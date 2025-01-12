from django.urls import path

from .views import BuyGoldView, SellGoldView, TransactionHistoryView

urlpatterns = [
    path("buy/", BuyGoldView.as_view(), name="buy-gold"),
    path("sell/", SellGoldView.as_view(), name="sell-gold"),
    path("user/", TransactionHistoryView.as_view(), name="history"),
]