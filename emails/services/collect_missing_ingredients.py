from stock.models import InventoryIngredient
from django.db import models

def find_missing_ingredients():
    ingredients = InventoryIngredient.objects.filter(minimum_stock_needed__lt=models.F('current_stock'))