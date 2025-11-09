from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Profile,
    PendingUser,
    Category,
    Product,
    ProductImage,
    ProductVariant,
    Cart,
    CartItem,
    Order,
    OrderItem,
    HomeHero,
)

admin.site.register(Profile)
admin.site.register(PendingUser)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


# ✅ Inline for adding multiple images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height: 120px; border-radius: 6px;" />', obj.image.url)
        return "No image uploaded"
    image_preview.short_description = "Current Image"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['size', 'stock']
    min_num = 0
    max_num = len(ProductVariant.Sizes.choices)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [ProductImageInline, ProductVariantInline]  # 👈 Enable multiple image uploads and size variants
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'price', 'is_available')
        }),
        ('Inventory', {
            'fields': ('stock',)
        }),
        ('Primary Image', {
            'fields': ('image',)
        }),
        ('Preview', {
            'fields': ('image_preview',),
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<div style="display:flex; gap:12px; align-items:center;">'
                '<img src="{}" style="max-height: 180px; border-radius: 8px;" />'
                '<span style="font-size: 13px; color: #555;">Preview of the current Cloudinary image.</span>'
                '</div>',
                obj.image.url,
            )
        return "Upload an image to preview"
    image_preview.short_description = "Current Image"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_item_count', 'get_total', 'created_at']

    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Items'

    def get_total(self, obj):
        return f"Rs.{obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'size', 'quantity', 'get_total']

    def get_total(self, obj):
        return f"Rs.{obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'payment_method', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'size', 'quantity', 'price', 'get_total']

    def get_total(self, obj):
        return f"Rs.{obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle')
        }),
        ('Buttons', {
            'fields': (
                ('primary_button_label', 'primary_button_url'),
                ('secondary_button_label', 'secondary_button_url'),
            )
        }),
        ('Meta', {
            'fields': ('updated_at',),
        }),
    )
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        return not HomeHero.objects.exists()

