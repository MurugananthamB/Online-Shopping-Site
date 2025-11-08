from django.urls import path
from . import views
from . import auth_views
from . import jwt_views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Traditional authentication URLs
    path('',views.login_view,name="login"),
    path('register',views.register_view,name="register"),
    path('accounts/registration-pending/', views.registration_pending, name='registration_pending'),
    path('home',views.homepage,name="homepage"),
    path('password-reset/', auth_views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # JWT Authentication URLs
    path('api/token/', jwt_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/login/', jwt_views.jwt_login, name='jwt_login'),
    path('api/user/', jwt_views.jwt_user_info, name='jwt_user_info'),
    
    # E-commerce URLs
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
