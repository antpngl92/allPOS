from django.shortcuts import render
from django.http import JsonResponse
from supplier.models import Supplier
from django.db import IntegrityError

# Create your views here.


def create_suplier_API(request):
    status = "Registration Successful"
    if request.method == "POST":
        data            = request.POST.getlist('data[]')
        supplier_name   = data[0]
        supplier_email  = data[1]
        supplier_number = data[2]
        lead_time       = data[3]

        # print(supplier_name)
        # print(supplier_email)
        # print(supplier_number)
        # print(lead_time)

        supplier = Supplier(name=supplier_name,email=supplier_email,phone=supplier_number, lead_time_delivery=lead_time)
        try:
            supplier.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                status = "Supplier with this name already exists"
    
    return JsonResponse({'status':status}, safe=False)