from django.db.models.signals import pre_save
from django.dispatch import receiver
from mini_avito_app import models


@receiver(pre_save, sender=models.Products)
def update_available_status(sender, instance, **kwargs):
    instance.available = instance.quantity > 0


@receiver(pre_save, sender=models.Order)
def handle_order(sender, instance, **kwargs):
    if instance.status == 'Cancelled':
        instance.delete()
