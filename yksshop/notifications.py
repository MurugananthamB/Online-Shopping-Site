
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
    """Get the site URL for email links"""
    if settings.ALLOWED_HOSTS:
        host = settings.ALLOWED_HOSTS[0]
        if 'localhost' in host or '127.0.0.1' in host:
            return f'http://{host}:8000'
        return f'https://{host}'
    return 'http://localhost:8000'


def send_email_notification(subject, template_name, context, recipient_email, recipient_name=None, fail_silently=True):
    """
    Send email notification to user
    
    Args:
        subject: Email subject
        template_name: Template file name (without .html)
        context: Dictionary with template variables
        recipient_email: Recipient email address
        recipient_name: Recipient name (optional)
        fail_silently: If True, don't raise exceptions (default: True to prevent worker timeouts)
    """
    try:
        # Render HTML email
        html_content = render_to_string(f'shop/emails/{template_name}.html', context)
        text_content = strip_tags(html_content)  # Plain text version
        
        # Create email with fail_silently to prevent worker timeouts
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        msg.attach_alternative(html_content, 'text/html')
        # Use fail_silently=True to prevent blocking the request if SMTP times out
        msg.send(fail_silently=fail_silently)
        
        return True
    except Exception as e:
        # Log error but don't raise to prevent worker crashes
        print(f"Error sending email to {recipient_email}: {e}")
        import traceback
        print(traceback.format_exc())
        return False


def send_whatsapp_notification(phone_number, message):
    """
    Send WhatsApp notification using Twilio API
    
    Args:
        phone_number: Phone number with country code (e.g., +919876543210)
        message: Message to send
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Check if WhatsApp is enabled
        if not getattr(settings, 'WHATSAPP_ENABLED', False):
            print("WhatsApp notifications are disabled")
            return False
        
        # Get Twilio credentials from settings
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        whatsapp_from = getattr(settings, 'TWILIO_WHATSAPP_FROM', None)
        
        if not all([account_sid, auth_token, whatsapp_from]):
            print("Twilio credentials not configured")
            return False
        
        # Format phone number (ensure it starts with +)
        if not phone_number.startswith('+'):
            # Assume Indian number if no country code
            if phone_number.startswith('0'):
                phone_number = '+91' + phone_number[1:]
            else:
                phone_number = '+91' + phone_number
        
        # Twilio WhatsApp API endpoint
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        # Prepare message
        payload = {
            'From': f'whatsapp:{whatsapp_from}',
            'To': f'whatsapp:{phone_number}',
            'Body': message
        }
        
        # Send request
        response = requests.post(
            url,
            auth=(account_sid, auth_token),
            data=payload,
            timeout=10
        )
        
        if response.status_code == 201:
            print(f"WhatsApp message sent successfully to {phone_number}")
            return True
        else:
            print(f"Error sending WhatsApp: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending WhatsApp notification: {e}")
        return False


def send_order_confirmation(order):
    """
    Send order confirmation notification via email and WhatsApp
    """
    user = order.user
    recipient_email = user.email
    recipient_name = user.get_full_name() or user.username
    
    # Get phone number from profile
    phone_number = None
    try:
        phone_number = user.profile.phone
    except:
        pass
    
    # Email notification
    email_context = {
        'order': order,
        'user': user,
        'order_items': order.items.all(),
        'site_url': get_site_url(),
    }
    
    email_subject = f"Order Confirmation - #{order.order_number} | YKS Men's Wear"
    send_email_notification(
        email_subject,
        'order_confirmation',
        email_context,
        recipient_email,
        recipient_name
    )
    
    # WhatsApp notification
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
    """
    Send order status update notification
    """
    user = order.user
    recipient_email = user.email
    recipient_name = user.get_full_name() or user.username
    
    # Get phone number
    phone_number = None
    try:
        phone_number = user.profile.phone
    except:
        pass
    
    # Status messages
    status_messages = {
        'processing': 'Your order is being processed',
        'shipped': 'Your order has been shipped!',
        'delivered': 'Your order has been delivered!',
        'cancelled': 'Your order has been cancelled',
    }
    
    status_emoji = {
        'processing': '⏳',
        'shipped': '🚚',
        'delivered': '✅',
        'cancelled': '❌',
    }
    
    # Email notification
    email_context = {
        'order': order,
        'user': user,
        'old_status': old_status,
        'status_message': status_messages.get(order.status, 'Order status updated'),
        'site_url': get_site_url(),
    }
    
    email_subject = f"Order #{order.order_number} Status Update - {order.get_status_display()} | YKS Men's Wear"
    send_email_notification(
        email_subject,
        'order_status_update',
        email_context,
        recipient_email,
        recipient_name
    )
    
    # WhatsApp notification
    if phone_number:
        emoji = status_emoji.get(order.status, '📦')
        whatsapp_message = (
            f"{emoji} *Order Status Update*\n\n"
            f"Order #: {order.order_number}\n"
            f"Status: {order.get_status_display()}\n"
            f"Total: Rs.{order.total_amount}\n\n"
            f"{status_messages.get(order.status, 'Your order status has been updated')}\n\n"
            f"Track your order: {get_site_url()}/order/{order.id}/"
        )
        send_whatsapp_notification(phone_number, whatsapp_message)


def send_product_back_in_stock(product, user_email=None, user_phone=None):
    """
    Send notification when product is back in stock
    """
    if user_email:
        email_context = {
            'product': product,
            'site_url': get_site_url(),
        }
        
        email_subject = f"{product.name} is Back in Stock! | YKS Men's Wear"
        send_email_notification(
            email_subject,
            'product_back_in_stock',
            email_context,
            user_email
        )
    
    if user_phone:
        whatsapp_message = (
            f"🎉 *Great News!*\n\n"
            f"{product.name} is back in stock!\n"
            f"Price: Rs.{product.price}\n"
            f"Stock: {product.stock} available\n\n"
            f"Shop now: {get_site_url()}/product/{product.slug}/"
        )
        send_whatsapp_notification(user_phone, whatsapp_message)


def send_order_shipped(order, tracking_number=None):
    """
    Send order shipped notification
    """
    user = order.user
    recipient_email = user.email
    recipient_name = user.get_full_name() or user.username
    
    phone_number = None
    try:
        phone_number = user.profile.phone
    except:
        pass
    
    # Email
    email_context = {
        'order': order,
        'user': user,
        'tracking_number': tracking_number,
        'site_url': get_site_url(),
    }
    
    email_subject = f"Your Order #{order.order_number} Has Been Shipped! | YKS Men's Wear"
    send_email_notification(
        email_subject,
        'order_shipped',
        email_context,
        recipient_email,
        recipient_name
    )
    
    # WhatsApp
    if phone_number:
        tracking_info = f"\nTracking: {tracking_number}" if tracking_number else ""
        whatsapp_message = (
            f"🚚 *Order Shipped!*\n\n"
            f"Order #: {order.order_number}\n"
            f"Your order is on the way!{tracking_info}\n\n"
            f"Expected delivery: 3-5 business days\n\n"
            f"Thank you for shopping with YKS Men's Wear! 🙏"
        )
        send_whatsapp_notification(phone_number, whatsapp_message)

