from django.urls import path
from epos.views import (
    home_view,
    get_products_API
    )

urlpatterns = [
    path('',home_view,name='home'),
    path('category/<int:pk>',get_products_API,name='category'),


]