from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='my_orders'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('cancel/<int:id>/', views.cancel_order, name='cancel_order'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('orders/', views.my_orders, name='orders'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('orders/', views.my_orders, name='my_orders'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('cod-success/', views.payment_success, name='cod_success'),
    
]
