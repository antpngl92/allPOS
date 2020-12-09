from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from employee.models import Employee
from employee.forms import AccountAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('/home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid:
            pin = request.POST['pin']
            pin = int(pin)
            user = Employee.objects.get(pin=pin)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form

    return render(request, 'employee/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

