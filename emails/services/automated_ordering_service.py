from django.db import models

from django.core.mail import send_mail

from typing import List

from stock.models import (
    InventoryIngredient,
    AutomatedOrdering
)

from emails.models import OrderEmail

from employee.models import Employee

from allPOS.email_settings import EMAIL_FROM_LOCAL_FILE


def automated_ordering_service():

    automated_ordering = AutomatedOrdering.objects.get(
        pk=1
    )

    if not automated_ordering.enable:
        return

    target_inventory_ingredients = find_missing_ingredients()

    generated_email_objects = generate_order_email_objects(
        automated_ordering_object=automated_ordering,
        ingredient_targets=target_inventory_ingredients
    )

    send_automated_ordering_emails(
        email_targets=generated_email_objects
    )

    if automated_ordering.email_confirmation:
        send_manager_notification_for_automated_order(
            email_targets=generated_email_objects
        )

    if not automated_ordering.record_orders:
        for generated_email_object in generated_email_objects:
            generated_email_object.delete()


def send_manager_notification_for_automated_order(
    *,
    email_targets: OrderEmail
):

    managers = Employee.objects.filter(
        permission_level=1
    )

    recepients = []

    for i in managers:
        recepients.append(i.email)

    email_objects = email_targets

    message = ""

    ordinal_numbers = [
        '1st',
        '2nd',
        '3rd',
        '4th',
        '5th',
        '6th',
        '7th',
        '8th',
        '9th',
        '10th',
        '11th',
        '12th',
        '13th',
        '14th'
    ]

    index_ordinal_numbers = 0

    for email_object in email_objects:
        message += ordinal_numbers[index_ordinal_numbers] + " email:" + "\n\n"
        message += "Sent to: " + email_object.send_to + "\n"
        message += "----------------- EMAIL BODY -------------------------------------------\n"
        message += email_object.email_body + "\n\n"
        message += "========================================================================\n"
        index_ordinal_numbers += 1

    send_mail(
            "Orders Made today:",
            message,
            EMAIL_FROM_LOCAL_FILE,
            recepients
        )


def send_automated_ordering_emails(
    *,
    email_targets: List[OrderEmail]
):

    for email_target in email_targets:
        message = email_target.email_body
        recepient = [email_target.send_to]
        send_mail(
            email_target.email_subject,
            message,
            EMAIL_FROM_LOCAL_FILE,
            recepient
        )


def generate_order_email_objects(
    *,
    automated_ordering_object: AutomatedOrdering,
    ingredient_targets: List[InventoryIngredient]
) -> List[OrderEmail]:

    suppliers_needed = []
    generated_email_objects = []

    for ingredient_target in ingredient_targets:
        supplier = ingredient_target.supplier

        if supplier not in suppliers_needed:
            suppliers_needed.append(supplier)

    email_subject = automated_ordering_object.subject

    for supplier in suppliers_needed:
        email_body = ""
        automated_ordering_object.email_text = ""
        ingredients = ingredient_targets.filter(
            supplier=supplier
        )

        for i in ingredients:
            automated_ordering_object.email_text += \
                i.name + ": " + str(i.unit_weight) + "gr. \n"
        automated_ordering_object.save()

        email_body += automated_ordering_object.email_greeting_text
        email_body += "\n\n" + automated_ordering_object.email_text
        email_body += "\n\n" + automated_ordering_object.email_footer_text

        order_email = OrderEmail.objects.create(
            send_to=supplier.email,
            email_subject=email_subject,
            email_body=email_body
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
