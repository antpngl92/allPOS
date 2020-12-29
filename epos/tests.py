import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse

from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC


class CreateOrderTests(StaticLiveServerTestCase):

    fixtures = ['employee/data.json', 'ingredient/data.json', 'order/data.json', 'orderitem/data.json', 
    'product/data-category.json', 'product/data-food-labels.json', 'product/data-product.json',
    'stock/data-inventory-ingredient-transaction.json', 'stock/data-inventory-ingredient.json',
    'supplier/data.json']
    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='epos/chromedriver_linux')
      
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()

        login_button            = self.browser.find_element_by_xpath('//button[normalize-space()="Login"]')
        clock_in_out_button     = self.browser.find_element_by_xpath('//button[normalize-space()="Clock In/Out"]')
        pin_input               = self.browser.find_element_by_id('pin')
        pin_code                = '1111'
        employee_name           = 'Anton N.'

        pin_input.send_keys(pin_code)
        time.sleep(1)
        clock_in_out_button.click()
        login_button.click()


    def tearDown(self):
        self.browser.close()
    
   
    def test_order_number(self):
        order_number               = "44"
        order_number_button        = self.browser.find_element_by_id('order-number-anchor')
        print(order_number_button)
        order_number_button.click()
        time.sleep(1)

        order_number_input          = self.browser.find_element_by_id('order-number-input')
        order_number_input.send_keys(order_number)

        save_changes_button         = self.browser.find_element_by_id('modal-order-number-button')
        save_changes_button.click()

        order_number_content        = self.browser.find_element_by_class_name('order-number').text

        self.assertEquals(order_number, order_number_content)


    def test_order_type(self):
        order_type_1 = "Have In"
        order_type_2 = "Take Out"

        order_type_button           = self.browser.find_element_by_id('order-type-anchor')
        order_type_button.click()
        time.sleep(1)
        order_type_1_button         = self.browser.find_element_by_id('have-in')
        time.sleep(1)
        order_type_1_button.click()
        time.sleep(1)
        save_changes_button         = self.browser.find_element_by_id('modal-order-type-button')
        time.sleep(1)
        save_changes_button.click()

        order_type_content          = self.browser.find_element_by_class_name('order-type').text
        time.sleep(1)
        self.assertEquals(order_type_1, order_type_content)

        order_type_button.click()
        order_type_2_button         = self.browser.find_element_by_id('take-out')
        time.sleep(1)
        order_type_2_button.click()
        time.sleep(1)
        save_changes_button.click()
        time.sleep(3)
        order_type_content          = self.browser.find_element_by_class_name('order-type').text
        self.assertEquals(order_type_2, order_type_content)

    def test_order_products(self):
        product_button            = self.browser.find_element_by_css_selector("button[data-name='Latte']")
        product_button.click()
        products_table_row        = self.browser.find_elements_by_class_name('product-name')[0].text
        self.assertEqual(products_table_row, 'Latte')

    
    def test_quantity_add_remove_product(self):
        product_button            = self.browser.find_element_by_css_selector("button[data-name='Latte']")
        product_button.click()
        products_table_row        = self.browser.find_elements_by_class_name('product-quantity')[0].text
        self.assertEqual(products_table_row, '1')

        add_button                = self.browser.find_elements_by_class_name('fa-plus')[0]
        add_button.click()
        products_table_row        = self.browser.find_elements_by_class_name('product-quantity')[0].text
        self.assertEqual(products_table_row, '2')

        remove_button             = self.browser.find_elements_by_class_name('fa-minus')[0]
        remove_button.click()
        products_table_row        = self.browser.find_elements_by_class_name('product-quantity')[0].text
        self.assertEqual(products_table_row, '1')
