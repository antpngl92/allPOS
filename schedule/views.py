from django.shortcuts import render
from schedule.models import Schedule
from datetime import date
from timestamp.models import TimeStapm
import datetime

from django.http import JsonResponse
from employee.models import Employee

# Create your views here.
def todays_schedule(request):
    
    today   = date.today()
    schedules = Schedule.objects.filter(work_date=today).order_by('employee')
    context = {
        'title':    'Scheduler',
        'schedules': schedules,
    }
    return render(request, 'epos/schedule.html', context)

def get_rota(request):
    employees = Employee.objects.all()
    context = {
        'employees' : employees,
        'title'     : 'Rota'
    }
    return render(request, 'epos/rota.html', context)

def get_timestamps_API(request, pk):
    if request.method == "GET":
        t = datetime.today()
        t = t.strftime("%Y-%m-%d")
        stamps = TimeStapm.objects.filter(datestamp=t).filter(employee=pk).order_by('employee').order_by('-timestamp')[:2]
        stamps = list(stamps.values())
        context = {
            'stamps':stamps
        }
    return JsonResponse(context, safe=False)


def get_schedule_for_rota_API(request):
    context = {}
    if request.method == "GET":
        week = request.GET.getlist('week[]')
        week = [w[:10] for w in week]
        schedules = Schedule.objects.filter(work_date__in=week).order_by("employee")
        schedules = list(schedules.values())
    return JsonResponse(schedules, safe=False)