from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser

from employee.models import Employee

class EmployeeBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        pin = kwargs['pin']
        try:
            employee = Employee.objects.get(pin=pin)
            return employee
        except Employee.DoesNotExist:
            pass