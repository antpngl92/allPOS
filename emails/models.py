from django.db import models


class OrderEmail(models.Model):

    datetime = models.DateTimeField(
        auto_now_add=True
    )

    send_to = models.CharField(
        max_length=60,
        blank=True,
    )

