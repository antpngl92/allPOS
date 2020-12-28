from django.contrib import admin
from employee.models import Employee

class EmployeeAdmin(admin.ModelAdmin):
     list_display = ['pk']
admin.site.register(Employee, EmployeeAdmin)