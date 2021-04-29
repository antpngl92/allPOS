from django.contrib import admin
from product.models import Product, Category


class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'category',
    )


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
    )


admin.site.register(Category, CategoryAdmin)
