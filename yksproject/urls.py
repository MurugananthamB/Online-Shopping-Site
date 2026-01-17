from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Web views (normal HTML pages)
    path('', include('yksshop.web_urls')),

    # API views (JWT, AJAX, etc.)
    path('api/', include('yksshop.api_urls')),

    # Optional: Django AllAuth
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
