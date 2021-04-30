from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import datetime
from datetime import datetime
from datetime import date

from employee.models import Employee

from timestamp.models import TimeStapm

from schedule.models import Schedule


@login_required
def todays_schedule(request):

    today = date.today()
    schedules = Schedule.objects.filter(work_date=today).order_by('employee')

    context = {
        'title': 'Scheduler',
        'schedules': schedules,
    }

    return render(request, 'epos/schedule.html', context)


@login_required
def get_rota(request):

    employees = Employee.objects.all()

    context = {
        'employees': employees,
        'title': 'Rota'
    }

    return render(request, 'epos/rota.html', context)


@login_required
def update_rota(request):
    context = {}
    weekdates = []
    today_date = datetime.today()
    year, week_num, day_of_week = today_date.isocalendar()

    for day in range(7):

        week_date = datetime.strptime(
            str(year) + "-W{}".format(week_num) + '-{}'.format(day),
            "%Y-W%W-%w"
        )
        weekdates.append(week_date)

    schedules = Schedule.objects.filter(work_date__range=[weekdates[1],weekdates[0]]).order_by('work_date')

    context = {
        'title': 'Update Rota',
        'schedules': schedules
    }

    return render(request, 'epos/update_rota.html', context)


def get_timestamps_API(request, pk):

    if request.method == "GET":

        t = datetime.today()
        t = t.strftime("%Y-%m-%d")

        stamps = TimeStapm.objects.filter(
            datestamp=t
        ).filter(
            employee=pk
        ).order_by(
            'employee'
        ).order_by(
            '-timestamp'
        )[:2]

        stamps = list(stamps.values())

        context = {
            'stamps': stamps
        }

    return JsonResponse(context, safe=False)


def get_schedule_for_rota_API(request):

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

            week_date = datetime.strptime(
                str(year) + "-W{}".format(data) + '-{}'.format(day),
                "%Y-W%W-%w"
            )

            weekdates.append(week_date)

        schedules = Schedule.objects.filter(work_date__range=[weekdates[1],weekdates[0]]).order_by('work_date')
        schedules = list(
            schedules.values_list(
                'id',
                'employee__first_name',
                'work_date',
                'start_work_hour',
                'end_work_hour',
                'employee'
            )
        )

    return JsonResponse({'schedules': schedules}, safe=False)


def get_schedule_API(request, pk):

    if request.method == "GET":

        schedule = Schedule.objects.filter(pk=pk)

        schedule = list(
            schedule.values_list(
                'id',
                'employee__first_name',
                'work_date',
                'start_work_hour',
                'end_work_hour',
                'employee'
            )
        )

        employees = Employee.objects.all()

        employees = list(
            employees.values_list(
                'id',
                'first_name',
                'last_name'
            )
        )

        data = {
            'schedules': schedule,
            'employees': employees
        }

    return JsonResponse(data, safe=False)


def update_schedule_API(request, pk):

    if request.method == "POST":

        data = request.POST.getlist('data[]')

        schedule_id = data[0]
        employee_id = data[1]
        shift_date = data[2]
        shift_start = data[3]
        shift_end = data[4]

        employee = Employee.objects.get(pk=employee_id)
        schedule = Schedule.objects.get(pk=schedule_id)

        schedule.employee = employee
        schedule.work_date = shift_date
        schedule.start_work_hour = shift_start
        schedule.end_work_hour = shift_end
        schedule.save()

    return JsonResponse({'status': 'Success'}, safe=False)


def create_schedule_API(request):

    if request.method == "POST":

        data = request.POST.getlist('data[]')

        employee_id = data[0]
        employee = Employee.objects.get(pk=employee_id)

        shift_date = data[1]
        shift_start = data[2]
        shift_end = data[3]

        schedule = Schedule(
            employee=employee,
            work_date=shift_date,
            start_work_hour=shift_start,
            end_work_hour=shift_end
        )

        schedule.save()

    return JsonResponse({'status': 'Success'}, safe=False)


def delete_schedule_API(request, pk):

    if request.method == "DELETE":

        schedule = Schedule.objects.get(pk=pk)
        schedule.delete()

    return JsonResponse({'status': 'Success'}, safe=False)


@login_required
def timestamp_view(request):

    timestamps = TimeStapm.objects.all().order_by('-datestamp')
    title = "Timestamps"

    context = {
        'timestamps': timestamps,
        'title': title
    }

    return render(request, 'epos/timestamp.html', context)


@login_required
def employee_reports_view(request):

    title = "Employee Reports"

    context = {'title': title}

    return render(request, 'epos/employee_reports.html', context)


@login_required
def generate_report_API(request):

    employees = []
    days = []
    hours = []

    if request.method == "GET":

        employee_pk = request.GET.get('employee')
        d = request.GET.get('date')
        date_from = request.GET.get('from')
        date_to = request.GET.get('to')

        if employee_pk != all:

            emp = Employee.objects.get(pk=employee_pk)
            employees.append(emp.get_full_short())

            if d:
                h = single_employee_single_day_working_hours(emp,d)

                hours.append(h)
                days.append(d)
            else:
                d, h = single_employee_total_period_hours(emp,date_from,date_to)

                days += days + d
                hours += h

        for h in range(len(hours)):
            hours[h] = str(hours[h])[:7]

        data = {
           'emp': employees,
           'days': list(days),
           'hours': list(hours)
        }

    return JsonResponse(data, safe=False)


def single_employee_single_day_working_hours(employee, d):

    clockedIn = TimeStapm.objects.get(
        employee=employee,
        datestamp=d,
        activity_type=1
    )

    clockedOut = TimeStapm.objects.get(
        employee=employee,
        datestamp=d,
        activity_type=2
    )

    return datetime.combine(date.today(), clockedOut.timestamp) - datetime.combine(date.today(), clockedIn.timestamp)


def single_employee_total_period_hours(employee, date_from, date_to):

    dates = []
    hours = []

    timestamps = TimeStapm.objects.filter(
        employee=employee,
        datestamp__range=[date_from, date_to]
    )

    date = set()
    for i in timestamps:
        date.add(i.datestamp)
    date = list(date)
    date = sorted(date)

    for d in date:
        dates.append(d)
        hours.append(single_employee_single_day_working_hours(employee,d))

    return dates, hours
