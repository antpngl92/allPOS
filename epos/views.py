from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.core import serializers

from product.models import Product, Category
from employee.models import Employee
from orderitem.models import OrderItem
from order.models import Order


@login_required
def home_view(request):
    categories  = Category.objects.all()                                            # Get all categories 
    selected_category = categories.first()                                          # Get the first category which will be selected by default 
    order_items = OrderItem.objects.filter(product__category=selected_category.id)   # Get the order_items for the selected category
    user        = request.user
    title       = "EPOS"
    context = {
        'categories'        : categories,
        'user'              : user,   
        'title'             : title, 
        'order_items'       : order_items,
        'selected_category' : selected_category,
    }
    return render(request, 'epos/index.html', context)


def get_products_API(request, pk):
    if request.method == "GET":
        primary_key = pk
        order_items = OrderItem.objects.filter(product__category=primary_key)
        order_items = list(order_items.values())
    return JsonResponse(order_items, safe=False)

def create_order_API(request, pk):
    if request.method == "POST":
        order_item_pk = pk
        
        order, created = Order.objects.get_or_create()

