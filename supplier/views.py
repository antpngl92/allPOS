from django.shortcuts import render
from django.http import JsonResponse
from supplier.models import Supplier
from django.db import IntegrityError

# Create your views here.


def get_suppliers_API(request):
    suppliers = []
    if request.method == 'GET':
        suppliers = list(Supplier.objects.all().values())
    return JsonResponse(suppliers, safe=False)

def create_suplier_API(request):
    status = "Registration Successful"
    if request.method == "POST":
        data            = request.POST.getlist('data[]')
        supplier_name   = data[0]
        supplier_email  = data[1]
        supplier_number = data[2]
        lead_time       = data[3]

        supplier = Supplier(name=supplier_name,email=supplier_email,phone=supplier_number, lead_time_delivery=lead_time)
        try:
            supplier.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                status = "Supplier with this name already exists"
    
    return JsonResponse({'status':status}, safe=False)