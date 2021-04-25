from django.contrib import admin
from ingredient.models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_quantity')


admin.site.register(Ingredient, IngredientAdmin)
