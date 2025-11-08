from django.apps import AppConfig


class YksshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yksshop'
    
    def ready(self):
        import yksshop.signals  # Register signals