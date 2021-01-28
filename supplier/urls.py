from django.urls import path
from supplier.views import (
        create_suplier_API
    )

urlpatterns = [

    path('supplier/',create_suplier_API,name='create supplier'),
]