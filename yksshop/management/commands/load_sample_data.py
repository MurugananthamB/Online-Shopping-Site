"""
Management command to load sample products and categories for YKS Men's Wear
Usage: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from yksshop.models import Category, Product, ProductVariant
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Loads sample categories and products for the e-commerce site'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to load sample data...'))
        
        # Create Categories
        categories_data = [
            {'name': 'Casual Shirts', 'description': 'Comfortable casual shirts for everyday wear'},
            {'name': 'Formal Shirts', 'description': 'Professional formal shirts for office and events'},
            {'name': 'Pants', 'description': 'Stylish pants and trousers'},
            {'name': 'Shorts', 'description': 'Comfortable shorts for casual wear'},
            {'name': 'T-Shirts', 'description': 'Classic and trendy t-shirts'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.name}'))
        
        # Sample Products Data
        products_data = [
            # Casual Shirts
            {
                'name': 'Blue Casual Shirt',
                'category': 'Casual Shirts',
                'price': 899.00,
                'stock': 50,
                'description': 'Comfortable blue casual shirt perfect for everyday wear. Made with premium cotton fabric.'
            },
            {
                'name': 'White Casual Shirt',
                'category': 'Casual Shirts',
                'price': 799.00,
                'stock': 45,
                'description': 'Classic white casual shirt, versatile and stylish for any occasion.'
            },
            {
                'name': 'Striped Casual Shirt',
                'category': 'Casual Shirts',
                'price': 999.00,
                'stock': 30,
                'description': 'Trendy striped casual shirt with modern design and comfortable fit.'
            },
            {
                'name': 'Checkered Casual Shirt',
                'category': 'Casual Shirts',
                'price': 1099.00,
                'stock': 25,
                'description': 'Stylish checkered pattern casual shirt for a smart casual look.'
            },
            {
                'name': 'Denim Casual Shirt',
                'category': 'Casual Shirts',
                'price': 1199.00,
                'stock': 0,  # Out of stock
                'description': 'Classic denim casual shirt, durable and fashionable.'
            },
            
            # Formal Shirts
            {
                'name': 'White Formal Shirt',
                'category': 'Formal Shirts',
                'price': 1299.00,
                'stock': 60,
                'description': 'Premium white formal shirt, perfect for office and formal events.'
            },
            {
                'name': 'Light Blue Formal Shirt',
                'category': 'Formal Shirts',
                'price': 1399.00,
                'stock': 55,
                'description': 'Elegant light blue formal shirt with professional finish.'
            },
            {
                'name': 'Navy Blue Formal Shirt',
                'category': 'Formal Shirts',
                'price': 1499.00,
                'stock': 40,
                'description': 'Sophisticated navy blue formal shirt for business meetings.'
            },
            {
                'name': 'Pink Formal Shirt',
                'category': 'Formal Shirts',
                'price': 1349.00,
                'stock': 35,
                'description': 'Stylish pink formal shirt, adds a touch of color to your wardrobe.'
            },
            {
                'name': 'Grey Formal Shirt',
                'category': 'Formal Shirts',
                'price': 1249.00,
                'stock': 0,  # Out of stock
                'description': 'Professional grey formal shirt, versatile and elegant.'
            },
            
            # Pants
            {
                'name': 'Black Formal Pants',
                'category': 'Pants',
                'price': 1999.00,
                'stock': 50,
                'description': 'Classic black formal pants, perfect for office and formal occasions.'
            },
            {
                'name': 'Navy Blue Pants',
                'category': 'Pants',
                'price': 1899.00,
                'stock': 45,
                'description': 'Comfortable navy blue pants with modern fit and style.'
            },
            {
                'name': 'Grey Chinos',
                'category': 'Pants',
                'price': 1799.00,
                'stock': 40,
                'description': 'Stylish grey chinos, perfect for smart casual look.'
            },
            {
                'name': 'Beige Pants',
                'category': 'Pants',
                'price': 1699.00,
                'stock': 30,
                'description': 'Elegant beige pants, versatile for various occasions.'
            },
            {
                'name': 'Brown Formal Pants',
                'category': 'Pants',
                'price': 2099.00,
                'stock': 0,  # Out of stock
                'description': 'Premium brown formal pants with excellent quality fabric.'
            },
            
            # Shorts
            {
                'name': 'Cargo Shorts',
                'category': 'Shorts',
                'price': 999.00,
                'stock': 60,
                'description': 'Comfortable cargo shorts with multiple pockets, perfect for casual wear.'
            },
            {
                'name': 'Denim Shorts',
                'category': 'Shorts',
                'price': 1199.00,
                'stock': 55,
                'description': 'Classic denim shorts, durable and stylish for summer.'
            },
            {
                'name': 'Cotton Shorts',
                'category': 'Shorts',
                'price': 799.00,
                'stock': 50,
                'description': 'Lightweight cotton shorts, comfortable for everyday wear.'
            },
            {
                'name': 'Athletic Shorts',
                'category': 'Shorts',
                'price': 899.00,
                'stock': 45,
                'description': 'Sporty athletic shorts, perfect for workouts and casual activities.'
            },
            {
                'name': 'Khaki Shorts',
                'category': 'Shorts',
                'price': 1099.00,
                'stock': 0,  # Out of stock
                'description': 'Stylish khaki shorts for a smart casual summer look.'
            },
            
            # T-Shirts
            {
                'name': 'White T-Shirt',
                'category': 'T-Shirts',
                'price': 499.00,
                'stock': 100,
                'description': 'Classic white t-shirt, essential wardrobe staple.'
            },
            {
                'name': 'Black T-Shirt',
                'category': 'T-Shirts',
                'price': 499.00,
                'stock': 95,
                'description': 'Versatile black t-shirt, goes with everything.'
            },
            {
                'name': 'Grey T-Shirt',
                'category': 'T-Shirts',
                'price': 549.00,
                'stock': 80,
                'description': 'Comfortable grey t-shirt with premium cotton fabric.'
            },
            {
                'name': 'Blue T-Shirt',
                'category': 'T-Shirts',
                'price': 599.00,
                'stock': 70,
                'description': 'Stylish blue t-shirt, perfect for casual outings.'
            },
            {
                'name': 'Striped T-Shirt',
                'category': 'T-Shirts',
                'price': 649.00,
                'stock': 0,  # Out of stock
                'description': 'Trendy striped t-shirt with modern design.'
            },
        ]
        
        # Create Products
        created_count = 0
        updated_count = 0
        
        apparel_categories = {'Casual Shirts', 'Formal Shirts', 'Pants', 'Shorts', 'T-Shirts'}

        for prod_data in products_data:
            category = categories[prod_data['category']]
            slug = slugify(prod_data['name'])
            
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': prod_data['name'],
                    'category': category,
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'description': prod_data['description'],
                    'is_available': prod_data['stock'] > 0
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {product.name} - Rs.{product.price} (Stock: {product.stock})'))
            else:
                # Update existing product
                product.category = category
                product.price = prod_data['price']
                product.stock = prod_data['stock']
                product.description = prod_data['description']
                product.is_available = prod_data['stock'] > 0
                product.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'  Updated: {product.name} - Rs.{product.price} (Stock: {product.stock})'))

            if prod_data['category'] in apparel_categories:
                variant_sizes = [
                    ProductVariant.Sizes.S,
                    ProductVariant.Sizes.M,
                    ProductVariant.Sizes.L,
                    ProductVariant.Sizes.XL,
                ]
                total_stock = prod_data['stock']
                per_variant = total_stock // len(variant_sizes) if variant_sizes else 0
                remainder = total_stock % len(variant_sizes) if variant_sizes else 0

                for index, size in enumerate(variant_sizes):
                    size_stock = per_variant + (1 if index < remainder else 0)
                    ProductVariant.objects.update_or_create(
                        product=product,
                        size=size,
                        defaults={'stock': size_stock}
                    )

                product.stock = product.total_stock
                product.is_available = product.total_stock > 0
                product.save(update_fields=['stock', 'is_available'])
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Sample data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'   - Categories: {len(categories)}'))
        self.stdout.write(self.style.SUCCESS(f'   - Products created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'   - Products updated: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'\n💡 Note: Product images need to be uploaded manually through Django Admin'))
        self.stdout.write(self.style.SUCCESS(f'   Images should be placed in: media/products/'))

