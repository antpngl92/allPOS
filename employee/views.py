from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import (
    login,
    authenticate,
    logout
)

from django.contrib.auth.decorators import login_required

from django.http import (
    JsonResponse,
    QueryDict
)

from django.db import IntegrityError

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

import datetime

from decimal import Decimal

from timestamp.models import TimeStapm
from employee.models import Employee
from employee.forms import AccountAuthenticationForm


def login_view(request):

    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect('home')

    if request.POST:

        form = AccountAuthenticationForm(request.POST)

        if form.is_valid:
            pin = request.POST['pin']
            pin = int(pin)
            clocked_in = True

            try:
                employee = Employee.objects.get(
                    pin=pin
                )

            except ObjectDoesNotExist:
                context['clocked'] = "Incorrect PIN!"
                context['login_form'] = form
                context['title'] = "Log in"
                return render(request, 'employee/login.html', context)

            today = datetime.date.today()

            try:
                timestamp = TimeStapm.objects.filter(
                    employee=employee,
                    datestamp=today
                )

                timestamp = timestamp.latest(
                    'timestamp'
                )

            except ObjectDoesNotExist:
                clocked_in = False

            if clocked_in:
                if timestamp.activity_type == 1:
                    user = authenticate(
                        request,
                        pin=pin
                    )

                    if user:
                        login(
                            request,
                            user,
                            backend='django.contrib.auth.backends.ModelBackend'
                        )

                        return redirect('home')

                else:
                    context['clocked'] = "Please, clock in first!"

            else:
                context['clocked'] = "Please, clock in first!"
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    context['title'] = "Login"

    return render(request, 'employee/login.html', context)


@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


def clock_in_out_API(request):

    if request.method == "POST":

        status = "Unsuccessful"
        pin = request.POST['pin']
        employee = Employee.objects.get(pin=pin)

        today = datetime.date.today()
        todays_time_stamp_exist = True
        now = datetime.time

        try:
            timestamp = TimeStapm.objects.filter(
                employee=employee,
                datestamp=today
            )
            timestamp = timestamp.latest('timestamp')

        except ObjectDoesNotExist:
            todays_time_stamp_exist = False


        if todays_time_stamp_exist is False:
            timestamp_clock_in = TimeStapm(
                employee=employee,
                activity_type=1,
                datestamp=today,
                timestamp=now,
                on_shift=True
            )

            timestamp_clock_in.save()
            status = "Clocked In!"

        else:
            if timestamp.activity_type == 1:
                timestamp_clock_out = TimeStapm(
                    employee=employee,
                    activity_type=2,
                    datestamp=today,
                    timestamp=now,
                    on_shift=False
                )

                timestamp_clock_out.save()
                status = "Clocked Out!"

            else:
                timestamp_clock_in = TimeStapm(
                    employee=employee,
                    activity_type=1,
                    datestamp=today,
                    timestamp=now,
                    on_shift=True
                )

                timestamp_clock_in.save()
                status = "Clocked In!"

    return JsonResponse({'status': status}, safe=False)


@login_required
def create_employee_API(request):

    status = "Created"

    if request.method == "POST":

        data = request.POST.getlist('data[]')

        first_name = data[0]
        middle_name = data[1]
        surname = data[2]
        dob = data[3]
        address = data[4]
        tel_number = data[5]
        email = data[6]
        position = data[7]
        pay_rate = data[8]
        start_date = data[9]

        if data[10] == "":
            end_date = None
        else:
            end_date = data[10]

        if data[11] == "true":
            is_employeed = True
        else:
            is_employeed = False

        nin = data[12]
        permission = data[13]
        pin = data[14]

        password = "as9dia9sdik(ASIDKLASJDasd0as9d"

        employee = Employee(
            first_name=first_name,
            second_name=middle_name,
            last_name=surname,
            date_of_birth=dob,
            address=address,
            tel_number=tel_number,
            email=email,
            position=position,
            hourly_pay_rate=pay_rate,
            start_date=start_date,
            end_date=end_date,
            is_employeed=is_employeed,
            nin=nin,
            permission_level=permission,
            pin=pin,
            password=password
        )

        try:
            employee.save()
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                status = "User with this pin exists"

    return JsonResponse({'status': status}, safe=False)


@login_required
def get_employees(request):

    employees = Employee.objects.all()
    title = "Employees"

    context = {
        'employees': employees,
        'title': title
    }

    return render(request, 'employee/employees.html', context)


@login_required
def get_employee_API(request, pk):

    if request.method == "GET":

        employee = Employee.objects.filter(pk=pk)
        data = serializers.serialize('json',employee)

    return JsonResponse(data, safe=False)


@login_required
def delete_employee_API(request, pk):
    status = "Unsuccess"
    if request.method == "DELETE":

        employee = Employee.objects.get(pk=pk)
        employee.delete()
        status = "Success"

    return JsonResponse({'status': status}, safe=False)


@login_required
def edit_employee_API(request, pk):
    status = "Unsuccess"
    if request.method == "PUT":

        data = QueryDict(request.body)
        data = data.getlist(
            'data[]'
        )

        first_name = data[0]
        middle_name = data[1]
        surname = data[2]
        dob = data[3]
        address = data[4]
        tel_number = data[5]
        email = data[6]
        position = data[7]
        pay_rate = data[8]
        pay_rate = Decimal(pay_rate)
        pay_rate = round(
            pay_rate,
            2
        )
        start_date = data[9]

        if data[10] == "":
            end_date = None
        else:
            end_date = data[10]

        if data[11] == "true":
            is_employeed = True
        else:
            is_employeed = False

        nin = data[12]
        permission = data[13]
        pin = data[14]

        password = "as9dia9sdik(ASIDKLASJDasd0as9d"

        Employee.objects.filter(
            pk=pk
        ).update(
            first_name=first_name,
            second_name=middle_name,
            last_name=surname,
            date_of_birth=dob,
            address=address,
            tel_number=tel_number,
            email=email,
            position=position,
            hourly_pay_rate=pay_rate,
            start_date=start_date,
            end_date=end_date,
            is_employeed=is_employeed,
            nin=nin,
            permission_level=permission,
            pin=pin,
            password=password
        )
        status = "Success"

    return JsonResponse({'status': status}, safe=False)


def get_all_employees_API(request):

    if request.method == "GET":

        employees = Employee.objects.all()
        employees = list(employees.values_list('id','first_name','last_name'))

    return JsonResponse(employees, safe=False)
