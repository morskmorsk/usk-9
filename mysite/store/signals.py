from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.db import transaction
from .models import UserProfile, OrderDetail, Return, Inventory, Payment, ShoppingCartDetail, WorkOrderDetail

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=OrderDetail)
def update_inventory_on_order(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            product_inventory = Inventory.objects.select_for_update().get(product=instance.product)
            product_inventory.quantity_available -= instance.quantity
            if product_inventory.quantity_available < 0:
                raise ValueError("Not enough stock available")
            product_inventory.save()

@receiver(post_save, sender=Return)
def update_inventory_on_return(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            product_inventory = Inventory.objects.select_for_update().get(product=instance.product)
            product_inventory.quantity_available += instance.quantity
            product_inventory.save()

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):
    if instance.payment_status == 'completed':
        instance.order.status = 'paid'  # Assuming 'paid' is a valid status for your Order model
        instance.order.save()
    # Add additional conditions for other payment statuses if necessary

@receiver(post_save, sender=ShoppingCartDetail)
def reserve_inventory(sender, instance, created, **kwargs):
    if created:
        product_inventory = Inventory.objects.get(product=instance.product)
        product_inventory.quantity_reserved += instance.quantity
        product_inventory.save()

# @receiver(post_save, sender=WorkOrderDetail)
# def update_inventory_on_work_order(sender, instance, created, **kwargs):
#     if created or instance.quantity_changed:
#         part_inventory = Inventory.objects.get(product=instance.part)
#         part_inventory.quantity_reserved += instance.quantity
#         part_inventory.save()

# @receiver(post_delete, sender=WorkOrderDetail)
# def release_inventory_on_work_order_delete(sender, instance, **kwargs):
#     part_inventory = Inventory.objects.get(product=instance.part)
#     part_inventory.quantity_reserved -= instance.quantity
#     part_inventory.save()