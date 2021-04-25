from django.shortcuts import render
from django.http import JsonResponse
from supplier.models import Supplier
from django.db import IntegrityError


def get_suppliers_view(request):
    suppliers = Supplier.objects.all()
    context = {
        'title': 'Suplliers',
        'suppliers': suppliers
    }
    return render(request, 'epos/suppliers.html', context)


def get_suppliers_API(request):
    suppliers = []
    if request.method == 'GET':
        suppliers = list(Supplier.objects.all().values())
    return JsonResponse(suppliers, safe=False)


def create_suplier_API(request):
    status = "Registration Successful"
    if request.method == "POST":
        data = request.POST.getlist('data[]')
        supplier_name = data[0]
        supplier_email = data[1]
        supplier_number = data[2]
        lead_time = data[3]

        supplier = Supplier(
            name=supplier_name,
            email=supplier_email,
            phone=supplier_number,
            lead_time_delivery=lead_time
        )

        try:
            supplier.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                status = "Supplier with this name already exists"

    return JsonResponse({'status': status}, safe=False)


def edit_supplier_API(request, pk):
    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        time = request.POST['time']

        supplier = Supplier.objects.get(pk=pk)

        supplier.name = name
        supplier.email = email
        supplier.phone = phone
        supplier.lead_time_delivery = time
        supplier.save()

    return JsonResponse({}, safe=False)


def delete_supplier_API(request, pk):
    if request.method == "DELETE":
        supplier = Supplier.objects.get(pk=pk)
        supplier.delete()

    return JsonResponse({}, safe=False)
