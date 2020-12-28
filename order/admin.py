from django.contrib import admin
from order.models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk','order_type', 'order_numer', 'date', 'time', 'employee']
admin.site.register(Order, OrderAdmin)
