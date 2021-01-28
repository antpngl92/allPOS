from django.urls import path
from employee.views import (
    login_view, 
    logout_view,
    get_employees,

    
    clock_in_out_API,
    create_employee_API,
    get_employee_API, 
    delete_employee_API,
    edit_employee_API,
    )

urlpatterns = [

    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    
    path('employees/',get_employees,name='employee'),

    path('create/',create_employee_API,name='create employee'),
    path('clock/',clock_in_out_API,name='clock'),
    path('employee/<int:pk>',get_employee_API,name='get employee'),
    path('employee/delete/<int:pk>',delete_employee_API,name='delete employee'),
    path('employee/update/<int:pk>',edit_employee_API,name='update employee'),
    
]