from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from datetime import date
import datetime
from datetime import timedelta

from collections import defaultdict

from product.models import Product, Category

from orderitem.models import OrderItem

from order.models import Order, Tax

from stock.models import InventoryIngredientTransaction


@login_required
def home_view(request):
    # Get all categories
    categories = Category.objects.all()

    # Get the first category which will be selected by default
    selected_category = categories.first()

    # Get the order_items for the selected category (first category)
    products = Product.objects.filter(
        category=selected_category.id
    )

    user = request.user

    tax = Tax.objects.latest('id')

    context = {
        'categories': categories,
        'user': user,
        'title': "EPOS",
        'products': products,
        'selected_category': selected_category,
        'tax': tax
    }

    return render(request, 'epos/index.html', context)


@login_required
def analytics_view(request):
    today = date.today()

    orders = Order.objects.filter(date=today)

    ordered_items = defaultdict(dict)

    for order in orders:

        products_in_order = order.products.filter()

        for product in products_in_order:

            temp_name = product.product_name
            temp_quantity = product.quantity

            if ordered_items[temp_name] == {}:
                ordered_items[temp_name] = temp_quantity


            else:
                ordered_items[temp_name] = \
                 ordered_items[temp_name] + temp_quantity

    ordered_items = dict(ordered_items)

    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    today_week_day = get_today_week_day(today)

    weeek_days_list = get_list_week_days(week_days, today_week_day)

    this_week_daily_revenue = []
    last_week_daily_revenue = []

    for i in range(0, 14):
        temp_date = today - timedelta(days=i)
        orders = Order.objects.filter(date=temp_date)
        today_total = get_total_for_day(orders, temp_date)
        if(i < 7):
            this_week_daily_revenue.insert(0, today_total)
        else:
            last_week_daily_revenue.insert(0, today_total)

    context = {
        'item': ordered_items,
        'week_day': week_days[today_week_day],
        'this_week_daily_revenue': this_week_daily_revenue,
        'last_week_daily_revenue': last_week_daily_revenue,
        'weeek_days_list': weeek_days_list,
        'title': "Analytics"
    }

    return render(request, 'epos/analytics.html', context)


# get a list of week days, where today is last index
def get_list_week_days(wd, twd):

    days_arr = []
    for i in range(6, -1, -1):
        days_arr.append(wd[twd-i])

    return days_arr


# Get the total Revenue for the "date" argument
def get_total_for_day(orders, date):

    today_total = 0
    for order in orders:
        today_total += order.total_amount

    return today_total


# get the number of the week day
def get_today_week_day(today):

    year = str(today)[:4]

    month = str(today)[5:7]

    day = str(today)[8:10]

    week_num = datetime.date(
        int(year),
        int(month),
        int(day)
    ).weekday()

    return week_num


@login_required
def get_products_API(request, pk):
    if request.method == "GET":

        products = Product.objects.filter(category=pk)
        products = list(products.values())

    return JsonResponse(products, safe=False)


@login_required
def create_order_API(request):
    if request.method == "POST":

        products = request.POST.getlist('products[]')
        products_quantity = request.POST.getlist('products_quantity[]')
        order_number = request.POST.get('order_number')
        order_type = request.POST.get('order_type')
        order_total = request.POST.get('order_total')

        products_str_arr = []
        for product in products:
            products_str_arr.append(product)

        products_quantity_int_arr = []
        for quantiry in products_quantity:
            products_quantity_int_arr.append(int(quantiry))

        order_items = []
        products_arr = []
        for i in range(len(products)):
            temp_product_name = products_str_arr[i]
            prod = Product.objects.get(name=temp_product_name)

            prod_quan = products_quantity_int_arr[i]

            order_item = OrderItem(
                product=prod,
                quantity=prod_quan
            )

            products_arr.append(prod)

            order_items.append(order_item)
            order_item.save()

        o_type = 1
        if order_type == "Have In":
            o_type = 2
        p_type = 1
        if p_type == "Card":
            p_type = 2


        current_user = request.user
        order = Order(
            order_type=o_type,
            order_numer=order_number,
            employee=current_user,
            total_amount=order_total,
            paid=True,
            payment_method=p_type
        )
        order.save()
        order.products.set(order_items)
        order.save()

        for order_item in order_items:

            temp_product_quantity = order_item.quantity
            temp_product = order_item.product

            ingredients_for_product = temp_product.ingredient.all()
            for i in ingredients_for_product: 

                transaction = InventoryIngredientTransaction(
                    inventory_ingredient=i.inventory_ingredient,
                    quantity=i.quantity*temp_product_quantity,
                    transaction=1,
                    reason="For order "+order_number
                )
                transaction.save()

                i.inventory_ingredient.current_stock = (
                    i.inventory_ingredient.current_stock -
                    i.quantity*temp_product_quantity
                )
                i.inventory_ingredient.save()

    return JsonResponse({}, safe=False)


def get_order_API(request, pk):
    product = []
    quantity = []
    price = []
    if request.method == 'GET':
        order = Order.objects.get(pk=pk)
        for o in order.products.all():
            product.append(str(o))
            quantity.append(o.quantity)
            price.append(o.product.retail_price)

    return JsonResponse({'p': product, 'q': quantity, 'rp': price}, safe=False)


def get_orders_list_API(request):
    orders = []
    if request.method == 'GET':
        orders = Order.objects.all()

    return JsonResponse(list(orders.values()), safe=False)


def settings(request):

    title = "Settings"
    try:
        tax = Tax.objects.latest('id')

    except Tax.DoesNotExist:
        tax = ""

    context = {
        'title': title,
        'tax': tax
    }

    return render(request, 'epos/settings.html', context)


def get_TAX_API(request):

    try:
        tax = Tax.objects.latest('id')
        tax = tax.tax

    except Tax.DoesNotExist:
        tax = 0.00

    return JsonResponse({'tax': tax}, safe=False)


def change_TAX_API(request, tax):

    if request.method == "POST":
        tax = Tax(tax=tax)
        tax.save()

    return JsonResponse({'status': "status"}, safe=False)
