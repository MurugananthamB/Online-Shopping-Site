from django.core.management.base import BaseCommand

from yksshop.models import Product, ProductImage


class Command(BaseCommand):
    help = (
        "Clears Cloudinary references from product media so you can re-upload using the "
        "current storage backend."
    )

    def handle(self, *args, **options):
        cleared_products = 0
        for product in Product.objects.all():
            fields_to_update = []

            if product.image:
                product.image = None
                fields_to_update.append('image')

            if fields_to_update:
                product.save(update_fields=fields_to_update)
                cleared_products += 1

        cleared_product_images = 0
        for product_image in ProductImage.objects.all():
            fields_to_update = []

            if product_image.image:
                product_image.image = None
                fields_to_update.append('image')

            if fields_to_update:
                product_image.save(update_fields=fields_to_update)
                cleared_product_images += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Cleared stored Cloudinary paths on {cleared_products} product(s) and "
                f"{cleared_product_images} related image(s)."
            )
        )

