from django.db import models
from employee.models import Employee
from orderitem.models import OrderItem

class Order(models.Model):
    TAKEAWAY = 1
    HAVEIN   = 2
    ORDERTYPE = (
        (TAKEAWAY, "Takeaway"),
        (HAVEIN, "Have in"),
    )

    CASH = 1
    CARD = 2
    PAYMENTMETHOD = (
        (CASH, "Cash"),
        (CARD, "Card"),
    )

    products        = models.ManyToManyField(OrderItem)
    order_type      = models.IntegerField(choices=ORDERTYPE)
    order_numer     = models.IntegerField(blank=True)
    date            = models.DateField(auto_now_add=True)
    time            = models.TimeField(auto_now_add=True)
    employee        = models.ManyToManyField(Employee)
    total_amount    = models.DecimalField(decimal_places=2, max_digits=6)
    paid            = models.BooleanField()
    payment_method  = models.IntegerField(choices=PAYMENTMETHOD)