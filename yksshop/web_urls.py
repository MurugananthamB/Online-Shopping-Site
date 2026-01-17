from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Authentication
    #path('', views.login_view, name="login"),
    path('', views.homepage, name="homepage"),
    path('register/', views.register_view, name="register"),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/registration-pending/', views.registration_pending, name='registration_pending'),

    # Password reset
    path('password-reset/', auth_views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # E-commerce pages
    path('home/', views.homepage, name="homepage"),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Payment routes
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
]
