from django.db.models.signals import pre_save
from django.dispatch import receiver
from . import models


@receiver(pre_save, sender=models.Products)
def update_available_status(sender, instance, **kwargs):
    if instance.quantity <= 0:
        instance.available = False
    else:
        instance.available = True


@receiver(pre_save, sender=models.Order)
def handle_order(sender, instance, **kwargs):
    if instance.status == 'Cancelled':
        instance.delete()
