"""
Notification system for YKS Men's Wear
Handles Email and WhatsApp notifications for orders and products
"""
import os
import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_site_url():
    """Get the site URL for email links (always HTTPS in production)."""
    if not settings.DEBUG:
        # Force production domain + HTTPS
        return f"{settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}://yksshop.onrender.com"
    if settings.ALLOWED_HOSTS:
        host = settings.ALLOWED_HOSTS[0]
        if "localhost" in host or "127.0.0.1" in host:
            return f"http://{host}:8000"
        return f"https://{host}"
    return "http://localhost:8000"


def send_email_notification(subject, template_name, context, recipient_email, recipient_name=None, fail_silently=True):
    """
    Send email notification to user
    """
    try:
        # Prefix subject from settings (like "[YKS Men's Wear]")
        subject = f"{settings.ACCOUNT_EMAIL_SUBJECT_PREFIX.strip()} {subject}"

        # Render HTML + text
        html_content = render_to_string(f"shop/emails/{template_name}.html", context)
        text_content = strip_tags(html_content)

        # Ensure site_url is always present in template context
        context["site_url"] = get_site_url()

        # Create email
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,  # "YKS Men's Wear <no-reply@yksshop.com>"
            to=[recipient_email],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send(fail_silently=fail_silently)
        return True

    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")
        import traceback
        print(traceback.format_exc())
        return False


# -------------------------------------------------------
# WHATSAPP NOTIFICATIONS
# -------------------------------------------------------

def send_whatsapp_notification(phone_number, message):
    """Send WhatsApp notification using Twilio API."""
    try:
        if not getattr(settings, "WHATSAPP_ENABLED", False):
            print("WhatsApp notifications are disabled")
            return False

        account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", None)
        auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
        whatsapp_from = getattr(settings, "TWILIO_WHATSAPP_FROM", None)

        if not all([account_sid, auth_token, whatsapp_from]):
            print("Twilio credentials not configured")
            return False

        if not phone_number.startswith("+"):
            if phone_number.startswith("0"):
                phone_number = "+91" + phone_number[1:]
            else:
                phone_number = "+91" + phone_number

        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        payload = {
            "From": f"whatsapp:{whatsapp_from}",
            "To": f"whatsapp:{phone_number}",
            "Body": message,
        }

        response = requests.post(url, auth=(account_sid, auth_token), data=payload, timeout=10)
        if response.status_code == 201:
            print(f"WhatsApp sent successfully to {phone_number}")
            return True
        else:
            print(f"Error sending WhatsApp: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Error sending WhatsApp notification: {e}")
        return False


# -------------------------------------------------------
# ORDER EMAILS
# -------------------------------------------------------

def send_order_confirmation(order):
    """Send order confirmation via email + WhatsApp"""
    user = order.user
    recipient_email = user.email
    recipient_name = user.get_full_name() or user.username

    try:
        phone_number = user.profile.phone
    except:
        phone_number = None

    email_context = {
        "order": order,
        "user": user,
        "order_items": order.items.all(),
        "site_url": get_site_url(),
    }

    email_subject = f"Order Confirmation - #{order.order_number}"
    send_email_notification(
        email_subject,
        "order_confirmation",
        email_context,
        recipient_email,
        recipient_name,
    )

    if phone_number:
        whatsapp_message = (
            f"🎉 *Order Confirmed!*\n\n"
            f"Order #: {order.order_number}\n"
            f"Total: Rs.{order.total_amount}\n"
            f"Payment: {order.get_payment_method_display()}\n"
            f"Status: {order.get_status_display()}\n\n"
            f"Thank you for shopping with YKS Men's Wear! 🙏"
        )
        send_whatsapp_notification(phone_number, whatsapp_message)


def send_order_status_update(order, old_status=None):
    """Send order status update via email + WhatsApp"""
    user = order.user
    recipient_email = user.email
    recipient_name = user.get_full_name() or user.username

    try:
        phone_number = user.profile.phone
    except:
        phone_number = None

    status_messages = {
        "processing": "Your order is being processed",
        "shipped": "Your order has been shipped!",
        "delivered": "Your order has been delivered!",
        "cancelled": "Your order has been cancelled",
    }

    status_emoji = {
        "processing": "⏳",
        "shipped": "🚚",
        "delivered": "✅",
        "cancelled": "❌",
    }

    email_context = {
        "order": order,
        "user": user,
        "old_status": old_status,
        "status_message": status_messages.get(order.status, "Order status updated"),
        "site_url": get_site_url(),
    }

    email_subject = f"Order #{order.order_number} Status Update - {order.get_status_display()}"
    send_email_notification(email_subject, "order_status_update", email_context, recipient_email, recipient_name)

    if phone_number:
        emoji = status_emoji.get(order.status, "📦")
        whatsapp_message = (
            f"{emoji} *Order Status Update*\n\n"
            f"Order #: {order.order_number}\n"
            f"Status: {order.get_status_display()}\n"
            f"Total: Rs.{order.total_amount}\n\n"
            f"{status_messages.get(order.status, 'Your order status has been updated')}\n\n"
            f"Track your order: {get_site_url()}/order/{order.id}/"
        )
        send_whatsapp_notification(phone_number, whatsapp_message)
