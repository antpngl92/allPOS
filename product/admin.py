from django.contrib import admin
from product.models import Product, Category, FoodAllergenLabels


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', )
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
admin.site.register(Category, CategoryAdmin)

class FoodAllergenLabelsAdmin(admin.ModelAdmin):
    pass
admin.site.register(FoodAllergenLabels, FoodAllergenLabelsAdmin)