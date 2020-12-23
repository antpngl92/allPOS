from django.contrib import admin
from ingredient.models import Ingredient

# Register your models here.
# Register your models here.
class IngredientAdmin(admin.ModelAdmin):
    list_display=('name', 'get_quantity')
admin.site.register(Ingredient, IngredientAdmin)