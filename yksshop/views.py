from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import random

from .models import Profile, PendingUser, Category, Product, Cart, CartItem, Order, OrderItem
from .tokens import account_activation_token  # Ensure this is defined correctly
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

# Delete expired PendingUser entries (older than 5 minutes)
def delete_expired_pending_users():
    expiry = timezone.now() - timedelta(minutes=5)
    PendingUser.objects.filter(otp_created_at__lt=expiry).delete()




def register_view(request):
    delete_expired_pending_users()

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1 != password2:
            return render(request, 'shop/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(email=email).exists() or PendingUser.objects.filter(email=email).exists():
            return render(request, 'shop/register.html', {'error': 'Email is already registered or pending verification'})

        otp = str(random.randint(100000, 999999))
        hashed_password = make_password(password1)

        PendingUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            otp=otp,
            password_hash=hashed_password
        )

        # Send OTP email
        html_content = render_to_string('shop/send_otp_email.html', {
            'first_name': first_name,
            'otp': otp,
        })

        msg = EmailMultiAlternatives(
            subject='Verify your YKS Shop account with OTP',
            body='',
            from_email='no-reply@yks.com',
            to=[email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return render(request, 'shop/enter_otp.html', {'email': email})

    return render(request, 'shop/register.html')


def verify_otp_view(request):
    delete_expired_pending_users()

    if request.method == 'POST':
        email = request.POST.get('email')
        otp_input = request.POST.get('otp')

        try:
            pending_user = PendingUser.objects.get(email=email)

            if pending_user.otp == otp_input:
                pending_user.is_email_verified = True
                pending_user.save()

                # Generate fake user to sign token
                fake_user = User(username=pending_user.email, email=pending_user.email, is_active=False)
                fake_user.pk = hash(pending_user.email) % (10 ** 8)

                uid = urlsafe_base64_encode(force_bytes(fake_user.pk))
                token = account_activation_token.make_token(fake_user)

                activation_link = request.build_absolute_uri(
                    reverse('activate', kwargs={'uidb64': uid, 'token': token})
                )

                html_content = render_to_string('shop/activation_email.html', {
                    'activation_link': activation_link,
                    'user': pending_user,
                })

                msg = EmailMultiAlternatives(
                    subject='Activate your YKS Shop account',
                    body='',
                    from_email='no-reply@yks.com',
                    to=[email]
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

                return render(request, 'shop/registration_pending.html')

            else:
                return render(request, 'shop/enter_otp.html', {'error': 'Invalid OTP', 'email': email})

        except PendingUser.DoesNotExist:
            return redirect('register')

    return redirect('register')


def activate_view(request, uidb64, token):
    delete_expired_pending_users()

    try:
        for pending_user in PendingUser.objects.filter(is_email_verified=True):
            fake_user = User(username=pending_user.email, email=pending_user.email, is_active=False)
            fake_user.pk = hash(pending_user.email) % (10 ** 8)

            if urlsafe_base64_encode(force_bytes(fake_user.pk)) == uidb64:
                if account_activation_token.check_token(fake_user, token):
                    if User.objects.filter(email=pending_user.email).exists():
                        return render(request, 'shop/activation_invalid.html')

                    real_user = User.objects.create_user(
                        username=pending_user.email,
                        email=pending_user.email,
                        first_name=pending_user.first_name,
                        last_name=pending_user.last_name,
                        password=None  # set manually
                    )
                    real_user.password = pending_user.password_hash
                    real_user.is_active = True
                    real_user.save()

                    Profile.objects.update_or_create(user=real_user, defaults={'phone': pending_user.phone})
                    pending_user.delete()

                    return render(request, 'shop/activation_success.html')

        return render(request, 'shop/activation_invalid.html')
    except Exception as e:
        print("Activation error:", e)
        return render(request, 'shop/activation_invalid.html')


def login_view(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('homepage')
            else:
                error_message = 'Invalid password'
        except User.DoesNotExist:
            error_message = 'No user with this email'

    return render(request, 'shop/login.html', {'error_message': error_message})


def registration_pending(request):
    return render(request, 'shop/registration_pending.html')


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    
    # Get user orders
    orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'profile': profile,
        'recent_orders': orders,
    }
    return render(request, 'shop/profile.html', context)


# E-commerce Views
def homepage(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)[:12]  # Show 12 products on homepage
    
    # Get cart count for logged in users
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass
    
    context = {
        'categories': categories,
        'products': products,
        'cart_count': cart_count,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '')
    
    products = Product.objects.filter(is_available=True)
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'cart_count': cart_count,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug, is_available=True)
    except Product.DoesNotExist:
        return redirect('homepage')
    
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass
    
    context = {
        'product': product,
        'cart_count': cart_count,
    }
    return render(request, 'shop/product_detail.html', context)


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@require_POST
def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please login to add items to cart'})
    
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        product = Product.objects.get(id=product_id, is_available=True)
        
        if product.stock < quantity:
            return JsonResponse({'success': False, 'message': 'Insufficient stock'})
        
        cart = get_or_create_cart(request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
            cart_item.save()
        
        cart_count = cart.get_item_count()
        cart_total = float(cart.get_total())
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': cart_count,
            'cart_total': cart_total
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def view_cart(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_count': cart.get_item_count(),
    }
    return render(request, 'shop/cart.html', context)


@login_required
@require_POST
def update_cart(request):
    cart_item_id = request.POST.get('cart_item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
        else:
            if quantity > cart_item.product.stock:
                return JsonResponse({'success': False, 'message': 'Insufficient stock'})
            cart_item.quantity = quantity
            cart_item.save()
        
        cart = cart_item.cart
        cart_count = cart.get_item_count()
        cart_total = float(cart.get_total())
        item_total = float(cart_item.get_total()) if cart_item.quantity > 0 else 0
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'cart_total': cart_total,
            'item_total': item_total
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'})


@login_required
@require_POST
def remove_from_cart(request):
    cart_item_id = request.POST.get('cart_item_id')
    
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        
        cart_count = cart.get_item_count()
        cart_total = float(cart.get_total())
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'cart_total': cart_total
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'})


@login_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        return redirect('view_cart')
    
    # Get user profile for pre-filling
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'profile': profile,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
@require_POST
def place_order(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        return JsonResponse({'success': False, 'message': 'Your cart is empty'})
    
    # Get shipping details
    shipping_name = request.POST.get('shipping_name')
    shipping_phone = request.POST.get('shipping_phone')
    shipping_address = request.POST.get('shipping_address')
    shipping_city = request.POST.get('shipping_city')
    shipping_state = request.POST.get('shipping_state')
    shipping_pincode = request.POST.get('shipping_pincode')
    payment_method = request.POST.get('payment_method')
    
    if not all([shipping_name, shipping_phone, shipping_address, shipping_city, shipping_state, shipping_pincode, payment_method]):
        return JsonResponse({'success': False, 'message': 'Please fill all shipping details'})
    
    if payment_method not in ['online', 'cod']:
        return JsonResponse({'success': False, 'message': 'Invalid payment method'})
    
    # Check stock availability
    for item in cart_items:
        if item.quantity > item.product.stock:
            return JsonResponse({'success': False, 'message': f'Insufficient stock for {item.product.name}'})
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        payment_method=payment_method,
        total_amount=cart.get_total(),
        shipping_name=shipping_name,
        shipping_phone=shipping_phone,
        shipping_address=shipping_address,
        shipping_city=shipping_city,
        shipping_state=shipping_state,
        shipping_pincode=shipping_pincode,
    )
    
    # Create order items and update stock
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        # Update product stock
        item.product.stock -= item.quantity
        item.product.save()
    
    # Clear cart
    cart_items.delete()
    
    if payment_method == 'online':
        # In a real application, integrate with payment gateway here
        # For now, we'll just mark it as processing
        order.status = 'processing'
        order.save()
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully',
            'order_id': order.id,
            'redirect_url': f'/order-success/{order.id}/'
        })
    else:
        # Cash on delivery
        order.status = 'pending'
        order.save()
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully. You will pay on delivery.',
            'order_id': order.id,
            'redirect_url': f'/order-success/{order.id}/'
        })


@login_required
def order_success(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('homepage')
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'shop/order_list.html', context)


@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('order_list')
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_detail.html', context)
