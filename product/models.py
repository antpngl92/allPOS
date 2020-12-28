from django.db import models
from ingredient.models import Ingredient

class Product(models.Model):

    name                    = models.CharField(max_length=20)
    ingredient              = models.ManyToManyField(Ingredient)
    category                = models.ForeignKey('Category', null=True, blank=True, on_delete=models.DO_NOTHING)
    food_allergen_labels    = models.ManyToManyField('FoodAllergenLabels')
    retail_price            = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.name


    
    @property
    def actual_cost(self):    
        ingridients = Ingredient.objects.filter(product=self)
        print(f"Ingridients: {ingridients} for product: {self}")
        actual_cost = 0
        for i in ingridients:
            quantity = i.quantity
            inventory_ingredient = i.inventory_ingredient                       # get the inventory ingredient 
            inventory_ingredient_unit_cost = inventory_ingredient.unit_cost     # get the inventory ingredient unit cost 
            actual_cost += quantity * inventory_ingredient_unit_cost
        return actual_cost
    
   
class FoodAllergenLabels(models.Model):
    name        = models.CharField(max_length=20)
    milk        = models.BooleanField(default=False)
    soy         = models.BooleanField(default=False)
    eggs        = models.BooleanField(default=False)
    wheat       = models.BooleanField(default=False)
    fish        = models.BooleanField(default=False)
    peanuts     = models.BooleanField(default=False)
    shellfish   = models.BooleanField(default=False)
    Tree_nuts   = models.BooleanField(default=False)
    vegan       = models.BooleanField(default=False)
    vegeterian  = models.BooleanField(default=False)

    def __str__(self):
        return f"For : {self.name}"



class Category(models.Model):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField()
    parent      = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    slug        = models.SlugField(unique=True)

    class Meta:

        #enforcing that there can not be two categories under a parent with same slug
        # __str__ method elaborated later in post.  use __unicode__ in place of
        # __str__ if you are using python 2
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"
        ordering = ['id']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])