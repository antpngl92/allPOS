from django.contrib import admin
from orderitem.models import OrderItem

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'product_name']

admin.site.register(OrderItem, OrderItemAdmin)
