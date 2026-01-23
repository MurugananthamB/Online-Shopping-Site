from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class PendingUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    password_hash = models.CharField(max_length=128)
    otp = models.CharField(max_length=6)
    is_email_verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_image_url(self):
        if self.image:
            return self.image.url

        related_image = self.images.filter(image__isnull=False).first()
        if related_image and related_image.image:
            return related_image.image.url

        return 'https://via.placeholder.com/400x400?text=No+Image'

    @property
    def gallery_images(self):
        images = []

        if self.image:
            images.append(self.image.url)

        for related_image in self.images.all():
            if related_image.image:
                images.append(related_image.image.url)

        if not images:
            images.append('https://via.placeholder.com/400x400?text=No+Image')

        # Ensure uniqueness while preserving order
        seen = set()
        unique_images = []
        for url in images:
            if url not in seen:
                unique_images.append(url)
                seen.add(url)
        return unique_images

    @property
    def has_size_variants(self):
        return self.variants.exists()

    @property
    def total_stock(self):
        if self.has_size_variants:
            return sum(variant.stock for variant in self.variants.all())
        return self.stock

    def get_stock_for_size(self, size):
        if not size:
            return self.total_stock

        try:
            variant = self.variants.get(size=size)
            return variant.stock
        except ProductVariant.DoesNotExist:
            return 0


class ProductVariant(models.Model):
    class Sizes(models.TextChoices):
        XS = 'XS', 'XS'
        S = 'S', 'S'
        M = 'M', 'M'
        L = 'L', 'L'
        XL = 'XL', 'XL'
        XXL = 'XXL', 'XXL'

    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=10, choices=Sizes.choices)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')
        ordering = ['product', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        if self.size:
            return f"{self.quantity} x {self.product.name} ({self.size})"
        return f"{self.quantity} x {self.product.name}"

    def get_total(self):
        return self.product.price * self.quantity

    @property
    def available_stock(self):
        return self.product.get_stock_for_size(self.size)


class HomeHero(models.Model):
    title = models.CharField(max_length=150, default="Premium Men's Wear Collection")
    subtitle = models.CharField(
        max_length=255,
        default="Discover the latest styles and timeless classics"
    )
    primary_button_label = models.CharField(max_length=80, default="Shop the Collection")
    primary_button_url = models.CharField(max_length=200, default="/shop/")
    secondary_button_label = models.CharField(max_length=80, blank=True, null=True)
    secondary_button_url = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage Hero Content"
        verbose_name_plural = "Homepage Hero Content"

    def __str__(self):
        return "Homepage Hero Content"

    @classmethod
    def get_solo(cls):
        try:
            hero, _ = cls.objects.get_or_create(pk=1)
            return hero
        except Exception:
            # Return a default instance if table doesn't exist yet (migrations not run)
            # This prevents 500 errors during initial deployment
            return cls(
                pk=1,
                title="Premium Men's Wear Collection",
                subtitle="Discover the latest styles and timeless classics",
                primary_button_label="Shop the Collection",
                primary_button_url="/shop/",
            )


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('online', 'Online Payment'),
        ('cod', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    shipping_name = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=10)

    # Razorpay payment fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random, string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        if self.size:
            return f"{self.quantity} x {self.product.name} ({self.size})"
        return f"{self.quantity} x {self.product.name}"

    def get_total(self):
        return self.price * self.quantity
