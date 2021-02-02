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
    get_timestamps_API,
    get_schedule_for_rota_API
    )

urlpatterns = [
    path('',home_view,name='home'),
    path('analytics/',analytics_view,name='analytics'),
    path('category/<int:pk>',get_products_API,name='category'),
    path('orders/',get_orders_list_API,name='orders'),
    path('order/',create_order_API,name='order'),
    path('get_order/<int:pk>', get_order_API, name="this_order"),
    path('tax/', get_TAX_API, name="tax"),
    path('tax/<str:tax>', change_TAX_API, name="change tax"),
    path('settings/',settings, name="settings"),
    path('schedule/',todays_schedule, name="schedule"),
    path('rota/',get_rota, name="get rota"),
    path('stamps/<int:pk>/',get_timestamps_API, name="get stamps"),
    path('schedules/',get_schedule_for_rota_API, name="get schedule for rota"),
]