from django.contrib import admin

from emails.models import OrderEmail

class OrderEmailAdmin(admin.ModelAdmin):
     list_display = ['pk']
admin.site.register(OrderEmail, OrderEmailAdmin)


