import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class IngredientTests(StaticLiveServerTestCase):

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
        self.browser.get(self.live_server_url+'/suppliers/')
        time.sleep(2)

    def tearDown(self):
        self.browser.quit()

    # def test_edit_supplier(self):
    #     supplier_test_pk = str(21)
    #     suplier_test_name = "Test Supplier"
    #     supplier_test_email = "test@test.com"
    #     supplier_test_phone = "020 2020 2020"
    #     supplier_test_lead_time_delivery = 2

    #     supplier_edit_button = self.browser.find_elements_by_css_selector("button[data-id='"+supplier_test_pk+"']")
    #     supplier_edit_button[0].click()
    #     time.sleep(2)

    #     supplier_name_input = self.browser.find_element_by_id('supplier-name')
    #     supplier_name_input.clear()
    #     supplier_name_input.send_keys(suplier_test_name)


    #     supplier_email_input = self.browser.find_element_by_id('supplier-email')
    #     supplier_email_input.clear()
    #     supplier_email_input.send_keys(supplier_test_email)

    #     supplier_phone_input = self.browser.find_element_by_id('supplier-phone')
    #     supplier_phone_input.clear()
    #     supplier_phone_input.send_keys(supplier_test_phone)

    #     supplier_lead_time_delivery_input = self.browser.find_element_by_id('supplier-time')
    #     supplier_lead_time_delivery_input.clear()
    #     supplier_lead_time_delivery_input.send_keys(supplier_test_lead_time_delivery)

    #     update_supplier_button = self.browser.find_element_by_id('update-supplier-btn')
    #     update_supplier_button.click()

    #     supplier_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")
    #     import ipdb; ipdb.set_trace()
    #     self.assertEquals(supplier_row[0].text, suplier_test_name)
    #     self.assertEquals(supplier_row[1].text, supplier_test_email)
    #     self.assertEquals(supplier_row[2].text, supplier_test_phone)
    #     self.assertEquals(supplier_row[3].text, str(supplier_test_lead_time_delivery))

    # def test_delete_supplier(self):

    #     supplier_to_delete = str(21)

    #     supplier_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")
    #     supplier_name_before_deleting = supplier_row[0].text 

    #     ingredient_edit_button = self.browser.find_elements_by_css_selector("button[data-id='"+supplier_to_delete+"']")
    #     ingredient_edit_button[1].click()

    #     time.sleep(2)
    #     supplier_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")

    #     self.assertNotEquals(supplier_row[0].text, supplier_name_before_deleting)

    def test_create_supplier(self):

        self.browser.get(self.live_server_url+'/settings/')

        supplier_test_pk = str(21)
        suplier_test_name = "Test Supplier"
        supplier_test_email = "test@test.com"
        supplier_test_phone = "020 2020 2020"
        supplier_test_lead_time_delivery = 2

        supplier_name_input = self.browser.find_element_by_id('supplier_name_input')
        supplier_name_input.send_keys(suplier_test_name)

        supplier_email_input = self.browser.find_element_by_id('supplier_email_input')
        supplier_email_input.send_keys(supplier_test_email)

        supplier_phone_input = self.browser.find_element_by_id('supplier_number_input')
        supplier_phone_input.send_keys(supplier_test_phone)

        supplier_lead_time_delivery_input = self.browser.find_element_by_id('supplier_lead_time_input')
        supplier_lead_time_delivery_input.send_keys(supplier_test_lead_time_delivery)

        create_supplier_button = self.browser.find_element_by_id('create_supplier_button')
        create_supplier_button.click()
        time.sleep(3)

        self.browser.get(self.live_server_url+'/suppliers/')
        time.sleep(3)

        supplier_rows = self.browser.find_elements_by_xpath("//table/tbody/tr")
        last_supplier_row_num = str(len(supplier_rows))

        last_supplier_row = self.browser.find_elements_by_xpath("//table/tbody/tr["+last_supplier_row_num+"]/td")

        self.assertEquals(last_supplier_row[0].text,suplier_test_name)
        self.assertEquals(last_supplier_row[1].text,supplier_test_email)
        self.assertEquals(last_supplier_row[2].text,supplier_test_phone)
        self.assertEquals(last_supplier_row[3].text,str(supplier_test_lead_time_delivery))




