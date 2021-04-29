from django.contrib import admin

from order.models import Order, Tax


class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'order_numer',
        'total_amount',
        'order_type',
        'date',
        'time',
        'employee'
    ]


admin.site.register(Order, OrderAdmin)


class TaxAdmin(admin.ModelAdmin):

    list_display = [
        'pk',
        'tax'
    ]


admin.site.register(Tax, TaxAdmin)
