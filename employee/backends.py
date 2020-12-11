from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser

from employee.models import Employee

class EmployeeBackend(ModelBackend):

    def authenticate(self,request, pin):
        try:
            return Employee.objects.get(pin=pin)
        except Employee.DoesNotExist:
            return None

    def get_user(self, user_pk):
        try:
            return Employee.objects.get(pk=user_pk)
        except: 
            User.DoesNotExist
            return None