from django.db import models
from stock.models import InventoryIngredient


class Ingredient(models.Model):
    name = models.CharField(
        max_length=40, blank=False
    )
    quantity = models.DecimalField(
        blank=False,
        null=True,
        max_digits=5,
        decimal_places=3
    )
    inventory_ingredient = models.ForeignKey(
        InventoryIngredient,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_quantity(self):
        return str(self.quantity) + " kg"
