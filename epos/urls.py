from django.urls import path
from epos.views import (
    home_view,
    get_products_API,
    create_order_API
    )

urlpatterns = [
    path('',home_view,name='home'),
    path('category/<int:pk>',get_products_API,name='category'),
    path('order/',create_order_API,name='order'),


]