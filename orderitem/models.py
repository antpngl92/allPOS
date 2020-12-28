from django.db import models
from product.models import Product
from ingredient.models import Ingredient

class OrderItem(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    product_name    = models.CharField(max_length=30, blank=True)
    quantity        = models.IntegerField()
    

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.name
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name

   
