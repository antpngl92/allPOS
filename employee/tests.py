import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class EmployeeTests(StaticLiveServerTestCase):

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

    def tearDown(self):
        self.browser.quit()

    def test_login_when_clocked_in(self):
        pin_code = '1111'
        employee_name = 'Anton N.'

        login_button = self.browser.find_element_by_xpath(
            '//button[normalize-space()="Login"]'
        )

        clock_in_out_button = self.browser.find_element_by_xpath(
            '//button[normalize-space()="Clock In/Out"]'
        )

        pin_input = self.browser.find_element_by_id('pin')

        pin_input.send_keys(pin_code)
        clock_in_out_button.click()
        login_button.click()
        
        signed_employee_name = self.browser.find_element_by_id(
            'employee-full-short-name'
        ).text

        self.assertEqual(signed_employee_name,employee_name)

    def test_login_when_clocked_out(self):
        pin_code = '1111'

        login_button = self.browser.find_element_by_xpath(
            '//button[normalize-space()="Login"]'
        )

        pin_input = self.browser.find_element_by_id('pin')

        pin_input.send_keys(pin_code)
        login_button.click()
        clock_out_text = self.browser.find_element_by_id('clock').text

        time.sleep(3)

        self.assertEqual(clock_out_text,'Please, clock in first!')
