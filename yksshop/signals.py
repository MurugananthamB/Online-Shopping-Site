"""
Django signals for automatic notifications
Handles automatic email & WhatsApp notifications for orders and stock updates.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, Product
from .notifications import (  # ✅ note: use singular 'notification' (not notifications)
    send_order_confirmation,
    send_order_status_update,
    send_product_back_in_stock,
)

_old_order_status = {}


@receiver(pre_save, sender=Order)
def order_pre_save_handler(sender, instance, **kwargs):
    """
    Store old order status before saving, so we can detect status changes.
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
    Send notifications when an order is created or its status changes.
    - On creation: send order confirmation
    - On status update: send status update notification
    """
    try:
        if created:
            # 📨 Send order confirmation (email + WhatsApp)
            send_order_confirmation(instance)
        else:
            # Detect status change
            old_status = _old_order_status.pop(instance.pk, None)
            if old_status and instance.status != old_status:
                send_order_status_update(instance, old_status)
    except Exception as e:
        print(f"[Signal Error] order_post_save_handler: {e}")
        import traceback
        print(traceback.format_exc())


@receiver(pre_save, sender=Product)
def product_stock_handler(sender, instance, **kwargs):
    """
    Detect when a product that was out of stock comes back in stock.
    """
    if instance.pk:
        try:
            old_product = Product.objects.get(pk=instance.pk)
            if old_product.stock == 0 and instance.stock > 0 and instance.is_available:
                # ✅ Product is back in stock — trigger notification
                send_product_back_in_stock(instance)
        except Product.DoesNotExist:
            pass
