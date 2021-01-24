from django.db import models
from employee.models import Employee
# Create your models here.
class Schedule(models.Model):

    employee        = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    work_date       = models.DateField()
    start_work_hour = models.TimeField()
    end_work_hour   = models.TimeField()