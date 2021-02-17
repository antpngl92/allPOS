from django.shortcuts import render
from schedule.models import Schedule
from datetime import date
from timestamp.models import TimeStapm
import datetime
from datetime import datetime
from datetime import date
from django.http import JsonResponse
from employee.models import Employee
from django.core.exceptions import ObjectDoesNotExist
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

def update_rota(request):
    context = {}
    weekdates = []
    today_date = datetime.today()
    year, week_num, day_of_week = today_date.isocalendar()

    for day in range(7):
        week_date = datetime.strptime(str(year)+"-W{}".format(week_num)+ '-{}'.format(day), "%Y-W%W-%w")
        weekdates.append(week_date)

    schedules = Schedule.objects.filter(work_date__range=[weekdates[1], weekdates[0]]).order_by('work_date')
    context = {
        'title': 'Update Rota',
        'schedules' : schedules
    }
    return render(request, 'epos/update_rota.html', context)

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


def get_weekly_schedule_API(request):
    if request.method == "GET":
        data = request.GET['data']
        weekdates = []
        today_date = datetime.today()
        year, week_num, day_of_week = today_date.isocalendar()
        for day in range(7):
            week_date = datetime.strptime(str(year)+"-W{}".format(data)+ '-{}'.format(day), "%Y-W%W-%w")
            weekdates.append(week_date)
        schedules = Schedule.objects.filter(work_date__range=[weekdates[1], weekdates[0]]).order_by('work_date')      
        schedules = list(schedules.values_list('id', 'employee__first_name', 'work_date','start_work_hour','end_work_hour', 'employee'))
    return JsonResponse({'schedules':schedules}, safe=False)

def get_schedule_API(request, pk):
    if request.method == "GET":
        schedule = Schedule.objects.filter(pk=pk)
        schedule = list(schedule.values_list('id', 'employee__first_name', 'work_date','start_work_hour','end_work_hour' , 'employee'))
        employees = Employee.objects.all()
        employees = list(employees.values_list('id','first_name', 'last_name'))
        data = {
            'schedules' : schedule,
            'employees' : employees
        }

    return JsonResponse(data, safe=False)

def update_schedule_API(request, pk):
    if request.method == "POST":
        data = request.POST.getlist('data[]')
        schedule_id = data[0]
        employee_id = data[1]
        shift_date  = data[2]
        shift_start = data[3]
        shift_end   = data[4]
        employee = Employee.objects.get(pk=employee_id)

        schedule = Schedule.objects.get(pk=schedule_id)
        schedule.employee = employee
        schedule.work_date = shift_date
        schedule.start_work_hour = shift_start
        schedule.end_work_hour = shift_end
        schedule.save()
    
        return JsonResponse({'status':'Success'}, safe=False)
    return JsonResponse({'status':'Error'}, safe=False)

def create_schedule_API(request):
    if request.method == "POST":
        data = request.POST.getlist('data[]')
        employee_id = data[0]
        employee = Employee.objects.get(pk=employee_id)
        shift_date  = data[1]
        shift_start = data[2]
        shift_end   = data[3]
        schedule = Schedule(employee=employee, work_date=shift_date,start_work_hour=shift_start, end_work_hour=shift_end)
        schedule.save()

        return JsonResponse({'status':'Success'}, safe=False)
    return JsonResponse({'status':'Error'}, safe=False)

def delete_schedule_API(request, pk):
    if request.method == "DELETE":
        schedule = Schedule.objects.get(pk=pk)
        schedule.delete()
        return JsonResponse({'status':'Success'}, safe=False)
    return JsonResponse({'status':'Error'}, safe=False)
    