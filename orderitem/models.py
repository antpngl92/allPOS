from django.db import models
from product.models import Product
from ingredient.models import Ingredient

class OrderItem(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    product_name    = models.CharField(max_length=30, blank=True)
    retail_price    = models.DecimalField(decimal_places=2, max_digits=4)

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.name
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name

    @property
    def actual_cost(self):    
        ingridients = Ingredient.objects.filter(product=self.product)
        print(f"Ingridients: {ingridients} for product: {self}")
        actual_cost = 0
        for i in ingridients:
            quantity = i.quantity
            inventory_ingredient = i.inventory_ingredient                       # get the inventory ingredient 
            inventory_ingredient_unit_cost = inventory_ingredient.unit_cost     # get the inventory ingredient unit cost 
            actual_cost += quantity * inventory_ingredient_unit_cost
        return actual_cost
