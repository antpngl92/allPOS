from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from employee.models import Employee
from employee.forms import AccountAuthenticationForm
from timestamp.models import TimeStapm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import JsonResponse
from django.http import HttpResponse, Http404

# Create your views here.
def login_view(request):
    context     = {}
    user        = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid:
            pin         = request.POST['pin']
            pin         = int(pin) 
            clocked_in  = True # Assuming an employee is clocked in

            # Check if there is a user with the provided pin
            try:
                employee = Employee.objects.get(pin=pin) # get the employee with the pin
            except:
                context['clocked']      = "Incorrect PIN!"
                context['login_form']   = form
                context['title']        = "Log in"
                return render(request, 'employee/login.html', context)
            today = datetime.date.today() # get todays date 
            # get latest timestamp for today
            try:
                timestamp = TimeStapm.objects.filter(employee=employee, datestamp=today)
                timestamp = timestamp.latest('timestamp')
            except:
                clocked_in = False
            # if there is time stamp for today
            if clocked_in:
                # if the timestamp is clock in - the employee is clocked in and can log in
                if timestamp.activity_type == 1:
                    user = authenticate(request,pin=pin)
                    if user:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        return redirect('home')
                # if timestamp is clock out - the employee is clocked out and cannot log in
                else:
                    context['clocked'] = "Please, clock in first!"
            # if there is not time stamp for today
            else:
                context['clocked'] = "Please, clock in first!"
    else:
        form = AccountAuthenticationForm()
    context['login_form']       = form
    context['title']            = "Login"
    return render(request, 'employee/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def clock_in_out_API(request):
    if request.method == "POST":
        status      = "Unsuccessful"
        pin         = request.POST['pin']
        employee    = Employee.objects.get(pin=pin)
        today       = datetime.date.today() # get todays date
        todays_time_stamp_exist = True
        now         = datetime.time
        # Get the latest timestamp
        try:
            timestamp = TimeStapm.objects.filter(employee=employee, datestamp=today)
            timestamp = timestamp.latest('timestamp')
        except:
            todays_time_stamp_exist = False
        # If the employee doesn't have a timestamp for today create a clock in timestamp
        if todays_time_stamp_exist == False:
            timestamp_clock_in = TimeStapm(employee=employee, activity_type=1, datestamp=today, timestamp=now, on_shift=True)
            timestamp_clock_in.save()
            status = "Clocked In!"
        # If employee has timestamp for today
        else:
            # Check if employee is clocked in, if it is, clock out 
            if timestamp.activity_type == 1:
                timestamp_clock_out = TimeStapm(employee=employee, activity_type=2, datestamp=today, timestamp=now, on_shift=False)
                timestamp_clock_out.save()
                status = "Clocked Out!"
            # If employee is clocked out, clock in 
            else:
                timestamp_clock_in = TimeStapm(employee=employee, activity_type=1, datestamp=today, timestamp=now, on_shift=True)
                timestamp_clock_in.save()
                status = "Clocked In!"
    return JsonResponse({'status': status}, safe=False)