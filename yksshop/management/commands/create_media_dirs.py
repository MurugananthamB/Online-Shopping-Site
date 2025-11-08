"""
Django management command to create media directories
Run this after deployment to ensure media directories exist
"""
from django.core.management.base import BaseCommand
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Create media directories if they do not exist'

    def handle(self, *args, **options):
        # Create media root directory
        media_root = settings.MEDIA_ROOT
        products_dir = os.path.join(media_root, 'products')
        
        # Create directories
        os.makedirs(media_root, exist_ok=True)
        os.makedirs(products_dir, exist_ok=True)
        
        # Create .gitkeep files to ensure directories are tracked
        gitkeep_media = os.path.join(media_root, '.gitkeep')
        gitkeep_products = os.path.join(products_dir, '.gitkeep')
        
        if not os.path.exists(gitkeep_media):
            with open(gitkeep_media, 'w') as f:
                f.write('')
        
        if not os.path.exists(gitkeep_products):
            with open(gitkeep_products, 'w') as f:
                f.write('')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created media directories:'))
        self.stdout.write(f'  - {media_root}')
        self.stdout.write(f'  - {products_dir}')
