from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('accounts/login/', views.user_login),
path('logout/', views.user_logout, name='logout'), 
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:cart_id>/', views.remove_cart, name='remove'),

    path('checkout/', views.checkout, name='checkout'),  # ✅ FIXED
    path('place-order/', views.place_order, name='place_order'),
     ]