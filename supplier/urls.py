from django.urls import path
from supplier.views import (
        get_suppliers_view,
        create_suplier_API,
        get_suppliers_API,
        edit_supplier_API,
        delete_supplier_API
)

urlpatterns = [

    path('supplier/', create_suplier_API, name='create supplier'),
    path('supplier/get/all', get_suppliers_API, name='get suppliers'),
    path('suppliers/', get_suppliers_view, name='suppliers'),
    path('supplier/<int:pk>', edit_supplier_API, name='edit supplier'),
    path('supplier/delete/<int:pk>',delete_supplier_API,name='delete supplier'),
]
