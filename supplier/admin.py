from django.contrib import admin
from supplier.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'phone', 'lead_time_delivery')


admin.site.register(Supplier, SupplierAdmin)
