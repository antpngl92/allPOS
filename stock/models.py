from django.db import models
from supplier.models import Supplier

class InventoryIngredient(models.Model):
    name                 = models.CharField(max_length=30)
    supplier             = models.ManyToManyField(Supplier, blank=True) 
    unit_cost            = models.DecimalField(decimal_places=2, max_digits=4)
    unit_weight          = models.DecimalField(decimal_places=3, max_digits=5)
    current_stock        = models.DecimalField(blank=False, decimal_places=3, max_digits=5)
    minimum_stock_needed = models.DecimalField(blank=False, decimal_places=3, max_digits=5)

    def __str__(self):
        return self.name

class InventoryIngredientTransaction(models.Model):
    TAKEFROMSTOCK = 1
    ADDTOSTOCK    = 2
    TRANSACTIONTYPE = (
                        (TAKEFROMSTOCK, "Take from stock"),
                        (ADDTOSTOCK, "Add to stock")
    )
    inventory_ingredient    = models.ForeignKey(InventoryIngredient, on_delete=models.DO_NOTHING)
    quantity                = models.DecimalField(decimal_places=3, max_digits=5)
    transaction             = models.IntegerField(choices=TRANSACTIONTYPE)
    date                    = models.DateField(auto_now_add=True)
    time                    = models.TimeField(auto_now_add=True)
    reason                  = models.CharField(max_length=100)