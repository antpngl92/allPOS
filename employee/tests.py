import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse


class LoginTests(StaticLiveServerTestCase):

    fixtures = ['employee/data.json', 'ingredient/data.json', 'order/data.json', 'orderitem/data.json', 
    'product/data-category.json', 'product/data-food-labels.json', 'product/data-product.json',
    'stock/data-inventory-ingredient-transaction.json', 'stock/data-inventory-ingredient.json',
    'supplier/data.json', 'timestamp/data.json']


    
    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='epos/chromedriver_linux')
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.close()
    
    def test_login_when_clocked_in(self):
        login_button            = self.browser.find_element_by_xpath('//button[normalize-space()="Login"]')
        clock_in_out_button     = self.browser.find_element_by_xpath('//button[normalize-space()="Clock In/Out"]')
        pin_input               = self.browser.find_element_by_id('pin')
        pin_code                = '1111'
        employee_name           = 'Anton N.'

        pin_input.send_keys(pin_code)
        clock_in_out_button.click()
        login_button.click()

        signed_employee_name    = self.browser.find_element_by_id('employee-full-short-name').text
        self.assertEqual(signed_employee_name, employee_name)
    
    def test_login_when_clocked_out(self):
        login_button            = self.browser.find_element_by_xpath('//button[normalize-space()="Login"]')
        clock_in_out_button     = self.browser.find_element_by_xpath('//button[normalize-space()="Clock In/Out"]')
        pin_input               = self.browser.find_element_by_id('pin')
        pin_code                = '1111'
        employee_name           = 'Anton N.'

        
        pin_input.send_keys(pin_code)
        login_button.click()
        clock_out_text          = self.browser.find_element_by_id('clock').text
        time.sleep(3)
        self.assertEqual(clock_out_text, 'Please, clock in first!')



   