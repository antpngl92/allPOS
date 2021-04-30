from django.db import models
from employee.models import Employee


class Schedule(models.Model):

    employee = models.ForeignKey(Employee,null=True,on_delete=models.SET_NULL)
    work_date = models.DateField()
    start_work_hour = models.TimeField()
    end_work_hour = models.TimeField()

    def __str__(self):
        return self.employee.get_full_short()
