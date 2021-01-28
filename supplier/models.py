from django.db import models


class Supplier(models.Model):
    name                = models.CharField(max_length=30, unique=True)
    email               = models.CharField(max_length=30)
    phone               = models.CharField(max_length=20)
    lead_time_delivery  = models.IntegerField()

    def __str__(self):
        return f"{self.name}"
