import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class SendingEmailTests(StaticLiveServerTestCase):

    fixtures = [
        'fixtures/employee/employee_data.json',
        'fixtures/product/products_data.json',
        'fixtures/ingredient/ingredients_data.json',
        'fixtures/order/orders_data.json',
        'fixtures/order_item/order_items_data.json',
        'fixtures/stock/stock_data.json',
        'fixtures/schedule/schedule_data.json',
        'fixtures/supplier/supplier_data.json',
        'fixtures/timestamp/timestamp_data.json'
    ]

    def setUp(self):

        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    
    def test_send_email_service(self):
        from emails.models import OrderEmail
        from emails.services.automated_ordering_service import automated_ordering_service
        from stock.models import (
            InventoryIngredient,
            AutomatedOrdering
        )

        from decimal import Decimal

        ingredient = InventoryIngredient.objects.last()
        ingredient.current_stock = ingredient.minimum_stock_needed - Decimal(1.000) 
        ingredient.auto_ordering=True
        ingredient.save()

        settings = AutomatedOrdering.load()
        settings.enable = True 
        settings.record_orders = True
        settings.save()

        emails_sent = OrderEmail.objects.all()

        self.assertEqual(emails_sent.count(), 0)

        automated_ordering_service()

        self.assertEqual(emails_sent.count(), 1)






                
