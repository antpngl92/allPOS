from django.shortcuts import render

from django.http import JsonResponse
from decimal import Decimal

from product.models import (
    Product,
    Category
)

from ingredient.models import Ingredient

from supplier.models import Supplier

from stock.models import (
    InventoryIngredient,
    InventoryIngredientTransaction,
    AutomatedOrdering
)

from django.core.exceptions import ObjectDoesNotExist


def stock_view(request):

    inventory_ingredients = InventoryIngredient.objects.all()

    context = {
        'inventory_ingredients': inventory_ingredients,
        'title': "Inventory Ingredients"
    }

    return render(request, 'epos/inventory_ingredient.html', context)


def ingredient_view(request):

    ingredient = Ingredient.objects.all()

    context = {
        'ingredients': ingredient,
        'title': "Ingredients"
    }

    return render(request, 'epos/ingredient.html', context)


def stock_create_API(request):

    if request.method == "POST":

        new_name = request.POST.get('name').strip()
        new_supplier = request.POST.get('supplier')

        new_cost = Decimal(
            request.POST.get('cost').strip('"')
        )
        new_weight = Decimal(
            request.POST.get('weight').strip('"')
        )
        new_stock = Decimal(
            request.POST.get('stock').strip('"')
        )
        new_min_stock = Decimal(
            request.POST.get('min_stock').strip('"')
        )

        automated_ordering = request.POST.get('automated')

        if automated_ordering == "true":
            automated_ordering = True

        else:
            automated_ordering = False

        new_supplier = Supplier.objects.get(pk=new_supplier)

        new_inventory_ingredient = InventoryIngredient(
            name=new_name,
            supplier=new_supplier,
            unit_cost=new_cost,
            unit_weight=new_weight,
            current_stock=new_stock,
            minimum_stock_needed=new_min_stock,
            auto_ordering=automated_ordering
        )
        new_inventory_ingredient.save()

        data = {
            'pk': new_inventory_ingredient.pk,
            'sup': new_supplier.name,
        }

    return JsonResponse(data, safe=False)


def stock_delete_API(request, pk):

    if request.method == "DELETE":

        inventory_ingredient = InventoryIngredient.objects.get(pk=pk)

        inventory_ingredient.delete()
        status = "Successful"

    return JsonResponse({'status': status}, safe=False)


def stock_update_API(request, pk):

    if request.method == "POST":

        new_name = request.POST.get('name').strip()

        new_supplier = request.POST.get('supplier')

        new_cost = Decimal(
            request.POST.get('cost').strip()
        )
        new_weight = Decimal(
            request.POST.get('weight').strip()
        )
        new_stock = Decimal(
            request.POST.get('stock').strip()
        )
        new_min_stock = Decimal(
            request.POST.get('min_stock').strip()
        )

        automated_ordering = request.POST.get('automated')

        if automated_ordering == "true":
            automated_ordering = True

        else:
            automated_ordering = False

        new_supplier = Supplier.objects.get(pk=new_supplier)

        inventory_ingridient = InventoryIngredient.objects.get(pk=pk)

        InventoryIngredient.objects.filter(
            pk=pk
        ).update(
            name=new_name,
            supplier=new_supplier,
            unit_cost=new_cost,
            unit_weight=new_weight,
            current_stock=new_stock,
            minimum_stock_needed=new_min_stock,
            auto_ordering=automated_ordering
        )

        # Create a inventory transaction only if the quantity of the stock was
        # changed and record whoc changed it
        if inventory_ingridient.current_stock != new_stock:
            reason = f'{str(request.user.get_full_short())} \
                took stock using control panel'
            transaction_type = 1

            if inventory_ingridient.current_stock < new_stock:
                reason = f'{str(request.user.get_full_short())} \
                    added stock using control panel'
                transaction_type = 2

            transaction = InventoryIngredientTransaction(
                inventory_ingredient=inventory_ingridient,
                quantity=0.00,
                transaction=transaction_type,
                reason=reason
            )
            transaction.save()
        status = "Successful"

    return JsonResponse({'status': status}, safe=False)


def get_inventory_igredients_API(request):

    if request.method == 'GET':

        data = {
            'inventory_ingredients': list(
                InventoryIngredient.objects.all().values()
            )
        }

    return JsonResponse(data, safe=False)


def ingredient_update_API(request, pk):

    if request.method == "POST":

        name = request.POST.get('name').strip()

        quantity = Decimal(
            request.POST.get('quantity')
        )

        rii_pk = request.POST.get('rii_pk')

        ingredient_pk = pk

        rii = InventoryIngredient.objects.get(pk=rii_pk)

        Ingredient.objects.filter(pk=ingredient_pk).update(
            name=name,
            quantity=quantity,
            inventory_ingredient=rii
        )

        data = {
            'rii_name': rii.name
        }

    return JsonResponse(data, safe=False)


def ingredient_create_API(request):

    if request.method == "POST":

        name = request.POST.get('name').strip()

        quantity = Decimal(
            request.POST.get('quantity').strip()
        )

        rii_pk = request.POST.get('rii_pk')

        rii = InventoryIngredient.objects.get(pk=rii_pk)

        ingr = Ingredient(
            name=name,
            quantity=quantity,
            inventory_ingredient=rii
        )
        ingr.save()

        data = {
            'rii_name': rii.name,
            'pk': ingr.pk
        }
    return JsonResponse(data, safe=False)


def ingredient_delete_API(request, pk):

    if request.method == "DELETE":

        ingredient = Ingredient.objects.get(pk=pk)
        ingredient.delete()

    return JsonResponse({}, safe=False)


def get_ingredients_for_products_API(request):

    if request.method == "GET":
        ingredients = Ingredient.objects.all()

        product_pk = ""

        try:
            product_pk = request.GET.get('pk')

        except ObjectDoesNotExist:
            pass
        category = Category.objects.values('pk', 'name')

        if product_pk is None or product_pk == "":
            data = {
                'ingredients': list(ingredients.values('id', 'name')),
                'categories': list(category.values('pk', 'name')),
            }

        else:
            product = Product.objects.get(
                pk=product_pk
            )
            data = {
                'ingredients': list(ingredients.values('id', 'name')),
                'ingridients_product': list(product.ingredient.values('pk')),
                'product_category': product.category.pk,
                'categories': list(category.values('pk', 'name')),
                'name': product.name,
                'retail_price': product.retail_price
            }

    return JsonResponse(data, safe=False)


def update_product_API(request, pk):
    if request.method == "POST":

        name = request.POST.get('name').strip()

        ingredients = request.POST.getlist('ingredients[]')

        ingredients = Ingredient.objects.filter(name__in=ingredients)

        ingredients = ingredients.values('pk')

        category = request.POST.get('category')

        category = Category.objects.get(name=category)

        price = Decimal(
            request.POST.get('price')
        )

        product = Product.objects.get(pk=pk)

        product.name = name

        product.ingredient.clear()
        for i in ingredients:
            product.ingredient.add(i['pk'])

        product.category = category
        product.retail_price = price
        product.save()
        data = {}

    return JsonResponse(data, safe=False)


def create_product_API(request):
    if request.method == "POST":

        name = request.POST.get('name').strip()

        ingredients = request.POST.getlist('igredients[]')

        ingredients = Ingredient.objects.filter(name__in=ingredients)

        ingredients = ingredients.values('pk')

        category = request.POST.get('category')

        category = Category.objects.get(name=category)

        price = Decimal(
            request.POST.get('price')
        )

        product = Product(
            name=name,
            category=category,
            retail_price=price
        )
        product.save()

        for i in ingredients:
            product.ingredient.add(i['pk'])

        product.save()
        data = {
            'pk': product.pk,
            'cost': product.actual_cost
        }

    return JsonResponse(data, safe=False)


def delete_product_API(request, pk):

    if request.method == "DELETE":

        product = Product.objects.get(pk=pk)
        product.delete()

    return JsonResponse({}, safe=False)


def inventory_transactions_view(request):

    inventory_ingredient_transactions = \
        InventoryIngredientTransaction.objects.all().order_by('-id')

    context = {
        'transactions': inventory_ingredient_transactions,
        'title': "Inventory Ingredients Transactions"
    }

    return render(request, 'epos/inventory_transaction.html', context)


def get_automated_ordering_settings_API(request):

    if request.method == "GET":

        automated_ordering = AutomatedOrdering.objects.get(pk=1)

        data = {
            'enable': automated_ordering.enable,
            'email_confirmation': automated_ordering.email_confirmation,
            'record_orders': automated_ordering.record_orders,
            'subject': automated_ordering.subject,
            'email_greeting_text': automated_ordering.email_greeting_text,
            'email_footer_text': automated_ordering.email_footer_text
        }

    return JsonResponse(data, safe=False)


def update_autmated_ordering_settings_API(request):

    if request.method == "POST":

        enable = request.POST.get('enable')

        email_confirmation = request.POST.get('email_confirmation')

        record_orders = request.POST.get('record_orders')

        subject = request.POST.get('subject')

        email_greeting_text = request.POST.get('email_greeting_text')

        email_footer_text = request.POST.get('email_footer_text')

        automated_ordering = AutomatedOrdering.objects.get(pk=1)

        automated_ordering.enable = enable.capitalize()
        automated_ordering.email_confirmation = email_confirmation.capitalize()
        automated_ordering.record_orders = record_orders.capitalize()
        automated_ordering.subject = subject
        automated_ordering.email_greeting_text = email_greeting_text
        automated_ordering.email_footer_text = email_footer_text
        automated_ordering.save()

    return JsonResponse({}, safe=False)
