from django.db import models
from employee.models import Employee
# Create your models here.
class Schedule(models.Model):

    employee        = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    work_date       = models.DateField()
    start_work_hour = models.TimeField()
    end_work_hour   = models.TimeField()