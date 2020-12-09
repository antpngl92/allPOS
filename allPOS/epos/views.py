from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from django.contrib.auth import authenticate


@login_required
def home_view(request):
    context = {'user' : request.user}
    return render(request, 'epos/index.html', context)


    