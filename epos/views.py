from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.core import serializers
import json
from datetime import date
from collections import defaultdict

from product.models import Product, Category
from employee.models import Employee
from orderitem.models import OrderItem
from order.models import Order
from stock.models import InventoryIngredientTransaction
from stock.models import InventoryIngredient


@login_required
def home_view(request):
    categories          = Category.objects.all()                                            # Get all categories 
    selected_category   = categories.first()                                          # Get the first category which will be selected by default 
    products            = Product.objects.filter(category=selected_category.id)   # Get the order_items for the selected category
    user                = request.user
    title               = "EPOS"
    context = {
        'categories'        : categories,
        'user'              : user,   
        'title'             : title, 
        'products'          : products,
        'selected_category' : selected_category,
    }
    return render(request, 'epos/index.html', context)

@login_required
def analytics_view(request):
    today = date.today()
    orders = Order.objects.filter(date=today)
    ordered_items = defaultdict(dict)
    for i in orders:
        products_for_order = i.products.filter()

        for j in products_for_order:
            temp_name       = j.product_name 
            temp_quantity   = j.quantity
            
            if ordered_items[temp_name] == {}:
                ordered_items[temp_name] = temp_quantity
            else:
                ordered_items[temp_name] = ordered_items[temp_name] + temp_quantity
    ordered_items = dict(ordered_items)
   
    context = {
        'item'      : ordered_items,
    }    
    return render(request, 'epos/analytics.html', context)

@login_required
def get_products_API(request, pk):
    if request.method == "GET":
        primary_key = pk
        products    = Product.objects.filter(category=primary_key)
        products    = list(products.values())
    return JsonResponse(products, safe=False)

@login_required
def create_order_API(request):
    if request.method == "POST":
        products            = request.POST.getlist('products[]')            
        products_quantity   = request.POST.getlist('products_quantity[]')   

        order_number        = request.POST.get('order_number')
        order_type          = request.POST.get('order_type')
        order_total         = request.POST.get('order_total')
        payment_type        = request.POST.get('payment_type')

        # Convert Product string to str list
        products_str_arr = []
        for p in products:
            products_str_arr.append(p)

        # Convert quantity str list to int 
        products_quantity_int_arr = []
        for p in products_quantity:
            products_quantity_int_arr.append(int(p))

        # Create order_items with the products and their quantities 
        order_items = []
        products_arr = []
        for i in range(len(products)):
            temp_product_name = products_str_arr[i]
            prod        = Product.objects.get(name=temp_product_name) # Temp Product   
            prod_quan   = products_quantity_int_arr[i]                 # Temp quantity
            order_item = OrderItem(product=prod, quantity=prod_quan)  # Create new order items for the ordered products

            products_arr.append(prod)                               # Store all products for the order in an array
            order_items.append(order_item)                          # Store all order items for the order in an array
            
            order_item.save()

        o_type = 1
        if order_type == "Have In":
            o_type =2 
        p_type = 1
        if p_type == "Card":
            p_type = 2

        # Create Order
        current_user = request.user
        order = Order(order_type=o_type, order_numer=order_number, employee=current_user, total_amount=order_total, paid=True,payment_method=p_type )
        order.save()
        order.products.set(order_items) # Set the order_items for this order
        order.save()

        for oi in order_items:   # Each order item of a Order
            temp_product_quantity = oi.quantity # Has 1 or more of the same products
            temp_product = oi.product           # temp_product is a Product model instance
            ingredients_for_product = temp_product.ingredient.all()  # get all ingredients for each Product
            for i in ingredients_for_product: # For each ingredient in Product
                # For each Inventory Ingridient in Ingredient 
                # Create a transaction
                transaction = InventoryIngredientTransaction(inventory_ingredient=i.inventory_ingredient, quantity=i.quantity*temp_product_quantity, transaction=1, reason="For order "+order_number)
                transaction.save()
                # Exctract used Ingridient quantity for each Order Item from Inventory Ingredient
                i.inventory_ingredient.current_stock = (i.inventory_ingredient.current_stock - i.quantity*temp_product_quantity)
                i.inventory_ingredient.save()

    return JsonResponse({}, safe=False)

