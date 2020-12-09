from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from employee.models import Employee
from employee.forms import AccountAuthenticationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.
@csrf_exempt
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
            user = Employee.objects.get(pin=pin)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form

    return render(request, 'employee/login.html', context)

@csrf_exempt
def home_view(request):
    user = request.user
    context = {}
    print(user.is_authenticated)
    if not user.is_authenticated:
        return redirect('login')

        
    else:
        users = Employee.objects.all()
        context = {'e':users}        
       
    return render(request, 'employee/home.html', context)