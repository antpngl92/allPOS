from django.shortcuts import render
from stock.models import InventoryIngredient, InventoryIngredientTransaction
from ingredient.models import Ingredient
from supplier.models import Supplier
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.auth.models import User

# Create your views here.
def stock_view(request):
    inventory_ingredients = InventoryIngredient.objects.all()

    context = { 
        'inventory_ingredients': inventory_ingredients,
        'title'      : "Inventory Ingredients" 
    }

    return render(request, 'epos/inventory_ingredient.html', context)

def ingredient_view(request):
    ingredient = Ingredient.objects.all()

    context = { 
        'ingredients' : ingredient,
        'title': "Ingredients"
    }
    return render(request, 'epos/ingredient.html', context)

def stock_create_API(request):
    if request.method == "POST":
        new_name            = request.POST.get('name')
        new_supplier        = request.POST.get('supplier')
        new_cost            = Decimal(
                                request.POST.get('cost')
                                .strip('"')
                            )
        new_weight          = Decimal(
                                request.POST.get('weight')
                                .strip('"')
                            )
        new_stock           = Decimal(
                                request.POST.get('stock')
                                .strip('"')
                            )
        new_min_stock       = Decimal(
                                request.POST.get('min_stock')
                                .strip('"')
                            )
        automated_ordering  = request.POST.get('automated')

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

def stock_delete_API(request,pk):
    if request.method == "DELETE":
        inventory_ingredient = InventoryIngredient.objects.get(pk=pk)
        inventory_ingredient.delete()
        status = "Successful"

    return JsonResponse({'status':status}, safe=False)
    



def stock_update_API(request, pk):
    if request.method == "POST":
        new_name            = request.POST.get('name')
        new_supplier        = request.POST.get('supplier')
        new_cost            = Decimal(
                                request.POST.get('cost')
                                .strip('"')
                            )
        new_weight          = Decimal(
                                request.POST.get('weight')
                                .strip('"')
                            )
        new_stock           = Decimal(
                                request.POST.get('stock')
                                .strip('"')
                            )
        new_min_stock       = Decimal(
                                request.POST.get('min_stock')
                                .strip('"')
                            )
        automated_ordering  = request.POST.get('automated')

        if automated_ordering == "true": 
            automated_ordering = True 
        else:
            automated_ordering = False

   
        new_supplier = Supplier.objects.get(pk=new_supplier)
        
        inventory_ingridient = InventoryIngredient.objects.get(pk=pk)

        InventoryIngredient.objects.filter(pk=pk).update(
            name=new_name,
            supplier=new_supplier,
            unit_cost=new_cost,
            unit_weight=new_weight,
            current_stock=new_stock,
            minimum_stock_needed=new_min_stock,
            auto_ordering=automated_ordering
        )
        # Create a inventory transaction only if the quantity of the stock was changed and 
        # record whoc changed it
        if inventory_ingridient.current_stock != new_stock:
            reason = f'{str(request.user.get_full_short())} took stock using control panel'
            transaction_type = 1
            if inventory_ingridient.current_stock < new_stock:
                reason = f'{str(request.user.get_full_short())} added stock using control panel'
                transaction_type =2

            transaction = InventoryIngredientTransaction(
                inventory_ingredient=inventory_ingridient, 
                quantity=0.00,
                transaction=transaction_type,   
                reason=reason 
            )
            transaction.save()
        status = "Successful"

    return JsonResponse({'status':status}, safe=False)


def get_inventory_igredients_API(request):
    if request.method == 'GET':
        data = {
            'inventory_ingredients' : list(InventoryIngredient.objects.all().values())
        }
    return JsonResponse(data, safe=False) 