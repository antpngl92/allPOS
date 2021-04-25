from django.db import models

from django.core.mail import send_mail

from typing import List

from stock.models import (
    InventoryIngredient, 
    AutomatedOrdering
)

from supplier.models import Supplier

from emails.models import OrderEmail

def automated_ordering_service():

    automated_ordering = AutomatedOrdering.objects.get(
        pk=1
    )

    text = automated_ordering.email_text

    if not automated_ordering.enable:
        return 
    
    target_inventory_ingredients = find_missing_ingredients()

    if automated_ordering.record_orders:
        generated_email_objects = generate_order_email_objects(
            ingredient_targets=target_inventory_ingredients
        )
    
    send_emails(
        email_targets=generated_email_objects
    )
    

    
def send_emails(
    *,
    email_targets : List[OrderEmail]
):


    
def generate_order_email_objects(
    *,
    ingredient_targets : List[InventoryIngredient]
) -> List[OrderEmail]:
    suppliers_needed = []
    generated_email_objects = []

    for ingredient_target in ingredient_targets:
        supplier = ingredient_target.supplier

        if supplier not in suppliers_needed:
            suppliers_needed.append(supplier)

    print(suppliers_needed)
    for supplier in suppliers_needed:

        ingredients = ingredient_targets.filter(
            supplier=supplier
        )   


        order_email = OrderEmail.objects.create(
            send_to=supplier.email,
        )
        order_email.ingredients.set(ingredients)
        order_email.save()
        generated_email_objects.append(order_email)

    return generated_email_objects

def find_missing_ingredients() -> List[InventoryIngredient]:
    
    ingredients = InventoryIngredient.objects.filter(
        minimum_stock_needed__gt=models.F(
            'current_stock'
        ),
        auto_ordering=True
    )
    return ingredients




