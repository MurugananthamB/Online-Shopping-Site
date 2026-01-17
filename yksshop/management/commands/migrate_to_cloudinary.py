from django.core.management.base import BaseCommand
from cloudinary import config
from cloudinary.uploader import upload
from django.conf import settings
from yksshop.models import Product  # Replace with your actual app and model

# Configure Cloudinary from Django settings
config(
    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
)

class Command(BaseCommand):
    help = "Upload existing local images to Cloudinary"

    def handle(self, *args, **options):
        products = Product.objects.all()
        total = products.count()
        self.stdout.write(self.style.SUCCESS(f"Found {total} products."))

        for product in products:
            # Skip if image is already a Cloudinary URL
            if product.image and str(product.image).startswith('http'):
                self.stdout.write(f"Skipping Product {product.id}: already in Cloudinary")
                continue

            if product.image:
                try:
                    # Upload local image to Cloudinary
                    res = upload(product.image.path)
                    # Save Cloudinary URL back to model
                    product.image = res['secure_url']
                    product.save()
                    self.stdout.write(self.style.SUCCESS(f"Uploaded Product {product.id}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed Product {product.id}: {e}"))

        self.stdout.write(self.style.SUCCESS("Migration to Cloudinary complete!"))
