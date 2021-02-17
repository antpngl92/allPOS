from django.urls import path
from epos.views import (
    home_view,
    analytics_view,datetime, 
    settings, 

    get_products_API,
    create_order_API,
    get_orders_list_API,
    get_order_API,
    get_TAX_API,
    change_TAX_API
    )
from schedule.views import (
    todays_schedule, 
    get_rota,
    update_rota,
    get_timestamps_API,
    get_schedule_for_rota_API,
    get_weekly_schedule_API,
    get_schedule_API,
    update_schedule_API,
    create_schedule_API,
    delete_schedule_API
    )

urlpatterns = [
    path('',home_view,name='home'),
    path('analytics/',analytics_view,name='analytics'),
    path('settings/',settings, name="settings"),
    path('schedule/',todays_schedule, name="schedule"),
    path('rota/',get_rota, name="get rota"),
    path('update/rota/',update_rota, name="update rota"),


    path('category/<int:pk>',get_products_API,name='category'),
    path('orders/',get_orders_list_API,name='orders'),
    path('order/',create_order_API,name='order'),
    path('get_order/<int:pk>', get_order_API, name="this_order"),
    path('tax/', get_TAX_API, name="tax"),
    path('tax/<str:tax>', change_TAX_API, name="change tax"),
    path('stamps/<int:pk>/',get_timestamps_API, name="get stamps"),
    path('schedules/',get_schedule_for_rota_API, name="get schedule for rota"),
    path('weekly-schedules/',get_weekly_schedule_API, name="get weekly schedule"),
    path('schedule/<int:pk>',get_schedule_API, name="get schedule"),
    path('schedule/<int:pk>/update',update_schedule_API, name="update schedule"),
    path('schedule/create',create_schedule_API, name="create schedule"),
    path('schedule/delete/<int:pk>',delete_schedule_API, name="delete schedule"),
]