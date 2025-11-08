"""
Django signals for automatic notifications
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, Product
from .notifications import (
    send_order_confirmation,
    send_order_status_update,
    send_product_back_in_stock
)

# Store old status before save
_old_order_status = {}


@receiver(pre_save, sender=Order)
def order_pre_save_handler(sender, instance, **kwargs):
    """
    Store old status before saving
    """
    if instance.pk:
        try:
            old_order = Order.objects.get(pk=instance.pk)
            _old_order_status[instance.pk] = old_order.status
        except Order.DoesNotExist:
            pass


@receiver(post_save, sender=Order)
def order_post_save_handler(sender, instance, created, **kwargs):
    """
    Send notification when order is created or status changes
    """
    if created:
        # New order created
        send_order_confirmation(instance)
    else:
        # Order updated - check if status changed
        if instance.pk and instance.pk in _old_order_status:
            old_status = _old_order_status[instance.pk]
            if instance.status != old_status:
                send_order_status_update(instance, old_status)
            # Clean up
            del _old_order_status[instance.pk]


@receiver(pre_save, sender=Product)
def product_stock_handler(sender, instance, **kwargs):
    """
    Track product stock changes to notify when back in stock
    """
    if instance.pk:
        try:
            old_product = Product.objects.get(pk=instance.pk)
            # If product was out of stock (stock=0) and now has stock
            if old_product.stock == 0 and instance.stock > 0 and instance.is_available:
                # Product is back in stock
                # Note: In a real app, you'd want to notify users who were waiting
                # This would require a separate model to track "notify me" requests
                pass
        except Product.DoesNotExist:
            pass

