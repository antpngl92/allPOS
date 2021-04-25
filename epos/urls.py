from django.urls import path

from epos.views import (
    home_view,
    analytics_view,
    settings,
    get_products_API,
    create_order_API,
    get_orders_list_API,
    get_order_API,
    get_TAX_API,
    change_TAX_API,
)

from schedule.views import (
    todays_schedule,
    get_rota,
    update_rota,
    timestamp_view,
    employee_reports_view,
    get_timestamps_API,
    get_schedule_for_rota_API,
    get_weekly_schedule_API,
    get_schedule_API,
    update_schedule_API,
    create_schedule_API,
    delete_schedule_API,
    generate_report_API
)

from stock.views import (
    stock_view,
    ingredient_view,
    inventory_transactions_view,
    stock_update_API,
    stock_create_API,
    stock_delete_API,
    get_inventory_igredients_API,
    ingredient_update_API,
    ingredient_create_API,
    ingredient_delete_API,
    get_ingredients_for_products_API,
    update_product_API,
    create_product_API,
    delete_product_API,
    get_automated_ordering_settings_API,
    update_autmated_ordering_settings_API
)

from product.views import products_view

urlpatterns = [
    path(
        '',
        home_view,
        name='home'
    ),

    path(
        'analytics/',
        analytics_view,
        name='analytics'
    ),

    path(
        'settings/',
        settings,
        name="settings"
    ),

    path(
        'schedule/',
        todays_schedule,
        name="schedule"
    ),

    path(
        'rota/',
        get_rota,
        name="get rota"
    ),

    path(
        'update/rota/',
        update_rota,
        name="update rota"
    ),

    path(
        'timestamps/',
        timestamp_view,
        name="timestamps"
    ),

    path(
        'employee_reports/',
        employee_reports_view,
        name="employee reports"
    ),

    path(
        'inventory-engridients/',
        stock_view,
        name="inventory ingredients"
    ),

    path(
        'ingridients/',
        ingredient_view,
        name="ingredients"
    ),

    path(
        'products/',
        products_view,
        name="products"
    ),

    path(
        'transactions/',
        inventory_transactions_view,
        name="inventory ingredients transactions"
    ),

    path(
        'category/<int:pk>',
        get_products_API,
        name='category'
    ),

    path(
        'orders/',
        get_orders_list_API,
        name='orders'
    ),

    path(
        'order/',
        create_order_API,
        name='order'
    ),

    path(
        'get_order/<int:pk>',
        get_order_API,
        name="this_order"
    ),

    path(
        'tax/',
        get_TAX_API,
        name="tax"
    ),

    path(
        'tax/<str:tax>',
        change_TAX_API,
        name="change tax"
    ),

    path(
        'stamps/<int:pk>/',
        get_timestamps_API,
        name="get stamps"
    ),

    path(
        'schedules/',
        get_schedule_for_rota_API,
        name="get schedule for rota"
    ),

    path(
        'weekly-schedules/',
        get_weekly_schedule_API,
        name="get weekly schedule"
    ),

    path(
        'schedule/<int:pk>',
        get_schedule_API,
        name="get schedule"
    ),

    path(
        'schedule/<int:pk>/update',
        update_schedule_API,
        name="update schedule"
    ),

    path(
        'schedule/create',
        create_schedule_API,
        name="create schedule"
    ),

    path(
        'schedule/delete/<int:pk>',
        delete_schedule_API,
        name="delete schedule"
    ),

    path(
        'report/',
        generate_report_API,
        name="generate report"
    ),

    path(
        'stock/<int:pk>',
        stock_update_API,
        name='update ingredient'
    ),

    path(
        'stock/create',
        stock_create_API,
        name='create ingredient'
    ),

    path(
        'stock/<int:pk>/delete',
        stock_delete_API,
        name='delete ingredient'
    ),

    path(
        'inventory-engridients-get-all',
        get_inventory_igredients_API,
        name='get inventory ingredients'
    ),

    path(
        'update-ingredient/<int:pk>',
        ingredient_update_API,
        name="upgrade ingredient"
    ),

    path(
        'create-ingredient/',
        ingredient_create_API,
        name="create ingredient2"
    ),

    path(
        'delete-ingredient/<int:pk>',
        ingredient_delete_API,
        name="delete ingredient2"
    ),

    path(
        'product-ingredients',
        get_ingredients_for_products_API,
        name="get products ingredients"
    ),

    path(
        'product-update/<int:pk>',
        update_product_API,
        name="update product"
    ),

    path(
        'product-create/>',
        create_product_API,
        name="create product"
    ),

    path(
        'product-delete/<int:pk>',
        delete_product_API,
        name="delete product"
    ),

    path(
        'automated-ordering-settings',
        get_automated_ordering_settings_API,
        name="automated ordering"
    ),

    path(
        'automated-ordering-update-settings',
        update_autmated_ordering_settings_API,
        name="update automated ordering"
    ),
]
