from django.db import models


class OrderEmail(models.Model):

    datetime = models.DateTimeField(auto_now_add=True)
    send_to = models.CharField(max_length=60, blank=True)
    email_subject = models.CharField(max_length=200, blank=True)
    email_body = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.send_to
