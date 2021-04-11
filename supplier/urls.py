from django.urls import path
from supplier.views import (
        create_suplier_API,
        get_suppliers_API
    )

urlpatterns = [

    path('supplier/',create_suplier_API,name='create supplier'),
    path('supplier/get/all',get_suppliers_API,name='get suppliers'),
]