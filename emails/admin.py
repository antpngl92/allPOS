from django.contrib import admin

from emails.models import OrderEmail


class OrderEmailAdmin(admin.ModelAdmin):

     list_display = ['pk', 'datetime', 'send_to', 'email_subject']


admin.site.register(OrderEmail, OrderEmailAdmin)
