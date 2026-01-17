import random
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from yksshop.models import Product


class Command(BaseCommand):
    help = (
        "Assigns product images by randomly picking files from media/products. "
        "Only products without an image are updated unless --force is supplied."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Reassign an image even if the product already has one.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of products to update.",
        )

    def handle(self, *args, **options):
        images_dir = Path(settings.MEDIA_ROOT) / "products"
        if not images_dir.exists():
            raise CommandError(f"Directory not found: {images_dir}")

        image_files = sorted(
            [path for path in images_dir.iterdir() if path.is_file()]
        )

        if not image_files:
            raise CommandError(
                f"No image files found in {images_dir}. Add files and retry."
            )

        queryset = Product.objects.all().order_by("id")
        if not options["force"]:
            queryset = queryset.filter(Q(image__isnull=True) | Q(image=""))

        limit = options["limit"]
        if limit is not None:
            queryset = queryset[:limit]

        if not queryset:
            self.stdout.write(
                self.style.WARNING("No products required updating.")
            )
            return

        updated_count = 0

        for product in queryset:
            source_path = random.choice(image_files)
            with source_path.open("rb") as image_file:
                filename = f"{product.slug}_{source_path.name}"
                product.image.save(filename, File(image_file), save=True)
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Assigned images to {updated_count} product(s) using {len(image_files)} available file(s)."
            )
        )

