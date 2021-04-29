from django.shortcuts import render
from product.models import Product


def products_view(request):
    products = Product.objects.all()

    context = {
        'products': products,
        'title': 'Products'
    }

    return render(request, 'epos/products.html', context)
