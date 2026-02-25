from django.urls import path
from . import views

urlpatterns = [
    path('shop/<slug:slug>/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('ajax/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/submit/', views.checkout_submit, name='checkout_submit'),
    path('orders/', views.my_orders, name='my_orders'),
]
