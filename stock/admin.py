from django.contrib import admin
from stock.models import InventoryIngredient, InventoryIngredientTransaction

class InventoryIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'unit_cost', 'unit_weight', 'current_stock', 'minimum_stock_needed' )
admin.site.register(InventoryIngredient, InventoryIngredientAdmin)

class InventoryIngredientTransactionAdmin(admin.ModelAdmin):
     list_display = ('inventory_ingredient','transaction','quantity','reason', 'date','time')
admin.site.register(InventoryIngredientTransaction, InventoryIngredientTransactionAdmin)
