from django.contrib import admin
from schedule.models import Schedule

class ScheduleAdmin(admin.ModelAdmin):
     list_display = ['pk', 'employee', 'work_date', 'start_work_hour', 'end_work_hour']
admin.site.register(Schedule, ScheduleAdmin)