from django.db import models
from ingredient.models import Ingredient


class Product(models.Model):

    name = models.CharField(
        max_length=40
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        blank=True,
        related_name='product'
    )
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )

    retail_price = models.DecimalField(
        decimal_places=2,
        max_digits=5
    )

    def __str__(self):
        return self.name

    @property
    def actual_cost(self):
        ingridients = self.ingredient.all()
        actual_cost = 0
        for i in ingridients:
            quantity = i.quantity
            inventory_ingredient = i.inventory_ingredient
            inventory_ingredient_unit_cost = inventory_ingredient.unit_cost

            actual_cost = (actual_cost + (quantity * inventory_ingredient_unit_cost)/inventory_ingredient_unit_cost)
        return round(actual_cost, 2)


class Category(models.Model):
    name = models.CharField(
        max_length=200
    )
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
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
