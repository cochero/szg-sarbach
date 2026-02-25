from django.contrib import admin
from .models import Medicine, Order, OrderItem


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'price', 'is_active']
    list_filter = ['department', 'is_active']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_date', 'total', 'payment_method', 'status']
    list_filter = ['status', 'payment_method']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'item_name', 'quantity', 'subtotal']
