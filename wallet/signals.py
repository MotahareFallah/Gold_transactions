from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wallet


@receiver(post_save, sender=get_user_model())
def create_wallet(sender, instance, created, **kwargs):
    if created:
        # Create a new wallet for the user when a new user is created
        Wallet.objects.create(user=instance)
