from django.db import models
from supplier.models import Supplier
from emails.models import OrderEmail

class InventoryIngredient(models.Model):
    name = models.CharField(
        max_length=30
    )
    
    supplier = models.ForeignKey(
        Supplier, 
        null=True, 
        blank=True, 
        on_delete=models.DO_NOTHING,
        db_constraint=False
    ) 
    
    unit_cost = models.DecimalField(
        decimal_places=2, 
        max_digits=4
    )
    
    unit_weight = models.DecimalField(
        decimal_places=3, 
        max_digits=5
    )
    
    current_stock = models.DecimalField(
        blank=False, 
        decimal_places=3, 
        max_digits=5
    )
    
    minimum_stock_needed = models.DecimalField(
        blank=False, 
        decimal_places=3, 
        max_digits=5
    )

    auto_ordering = models.BooleanField(
        default=False,
    )

    email_sent = models.ForeignKey(
        OrderEmail,
        on_delete=models.DO_NOTHING,
        blank=True, 
        null=True,
        related_name='ingredients'
    )


    def __str__(self):
        return self.name

class InventoryIngredientTransaction(models.Model):
    TAKEFROMSTOCK = 1
    ADDTOSTOCK    = 2
    TRANSACTIONTYPE = (
                        (TAKEFROMSTOCK, "Take from stock"),
                        (ADDTOSTOCK, "Add to stock")
    )

    inventory_ingredient    = models.ForeignKey(
        InventoryIngredient, 
        on_delete=models.DO_NOTHING
    )

    quantity                = models.DecimalField(
        decimal_places=3, 
        max_digits=5
    )

    transaction             = models.IntegerField(
        choices=TRANSACTIONTYPE
    )

    date = models.DateField(
        auto_now_add=True
    )
    
    time                    = models.TimeField(
        auto_now_add=True
    )
    
    reason                  = models.CharField(
        max_length=100
    )

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class AutomatedOrdering(SingletonModel):
    enable = models.BooleanField()
    record_orders = models.BooleanField()
    email_confirmation = models.BooleanField()
    email_text = models.CharField(
        max_length=1000
    )


    def __str__(self):
        status = 'enabled' if self.enable else 'disabled'
        return f'Autometed orderins is {status}'
    
