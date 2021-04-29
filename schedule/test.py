import time
from decimal import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from datetime import date


class TestScheduleTest(StaticLiveServerTestCase):

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
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        time.sleep(1)
        login_button = self.browser.find_element_by_class_name('button1')

        clock_in_out_button = self.browser.find_element_by_class_name('button2')

        pin_input = self.browser.find_element_by_id('pin')

        pin_code = '1111'

        pin_input.send_keys(pin_code)
        time.sleep(1)
        clock_in_out_button.click()
        login_button.click()
        time.sleep(2)

    def tearDown(self):

        self.browser.close()

    def test_create_schedule(self):
        self.browser.get(self.live_server_url+"/update/rota/")
        time.sleep(2)
        today = date.today()
        # dd/mm/YY
        
        today_date = today.strftime("%Y-%m-%d")
        today_date2 = today.strftime("%d/%m/%Y")

        test_data = [
            "Anton Nyagolov",
            today_date,
            "10:00",
            "20:00",
        ]

        create_schedule_button = self.browser.find_element_by_class_name('create_schedule')
        create_schedule_button.click()

        time.sleep(2)

        select = Select(WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "sel1"))))
        select.select_by_visible_text(test_data[0])

        date_picker = self.browser.find_element_by_id('shift_date_input')
        date_picker.send_keys(today_date2)

        shit_start_input = self.browser.find_element_by_id('shift_start_input')
        shit_start_input.send_keys(test_data[2])

        shift_end_input = self.browser.find_element_by_id('shift_end_input')
        shift_end_input.send_keys(test_data[3])

        create_schedule_button = self.browser.find_element_by_id('create_schedule_button')
        time.sleep(2)
        create_schedule_button.click()

        time.sleep(2)
        rwdata = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")

        self.browser.get(self.live_server_url+"/rota/")

        today = date.today()
        # dd
        today_date = today.strftime("%d")

        calendar_today = self.browser.find_element_by_id('34')

        assert f"{test_data[2]} - {test_data[3]}" in calendar_today.text
       