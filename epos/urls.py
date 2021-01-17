from django.urls import path
from epos.views import (
    home_view,
    analytics_view,datetime, 
    get_products_API,
    create_order_API,
    get_orders_list_API,
    )

urlpatterns = [
    path('',home_view,name='home'),
    path('analytics/',analytics_view,name='analytics'),
    path('category/<int:pk>',get_products_API,name='category'),
    path('orders/',get_orders_list_API,name='orders'),
    path('order/',create_order_API,name='order'),


]