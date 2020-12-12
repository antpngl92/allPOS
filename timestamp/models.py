from django.db import models
from employee.models import Employee

# Create your models here.
class TimeStapm(models.Model):
    CLOCKIN = 1
    CLOCKOUT = 2

    TIMESTAMP = (
        (CLOCKIN, 'Clock In'),
        (CLOCKOUT, 'Clock Out')
    )

    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    activity_type = models.IntegerField(choices=TIMESTAMP, default=CLOCKIN)
    datestamp = models.DateField(auto_now_add=True)
    timestamp = models.TimeField(auto_now_add=True)
    on_shift = models.BooleanField(default=False)
    
    def to_date(self):
        return self.timestamp.date

    def __str__(self):
        return f"{self.employee} did a {self.activity_type} on {self.datestamp} at {self.timestamp}"