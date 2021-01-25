from django.urls import path
from employee.views import (
    login_view, 
    logout_view,

    
    clock_in_out_API,
    create_employee_API, 
    )

urlpatterns = [

    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('clock/',clock_in_out_API,name='clock'),
    path('create/',create_employee_API,name='create employee'),
   
   

]