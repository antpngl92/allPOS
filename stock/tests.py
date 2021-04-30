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
        self.browser.get(self.live_server_url+'/inventory-engridients/')
        time.sleep(2)

    def tearDown(self):
        self.browser.quit()

    def test_edit_inventory_ingredient(self):

        inventory_ingredient_test_name = 'Test Inventory Ingredient'
        inventory_ingredient_test_supplier = 'Baker House'
        inventory_ingredient_test_unit_cost = '1.00'
        inventory_ingredient_test_unit_weight = '1.000'
        inventory_ingredient_test_unit_current_stock = '1.000'
        inventory_ingredient_test_minimum_stock_needed = '1.00'

        inventory_ingredient_to_edit_pk = str(1)

        ingredient_edit_button = self.browser.find_elements_by_css_selector("button[data-id='"+inventory_ingredient_to_edit_pk+"']")
        ingredient_edit_button[0].click()
        time.sleep(2)

        ingredient_name_input = self.browser.find_element_by_id('ing-name')
        ingredient_name_input.clear()
        ingredient_name_input.send_keys(inventory_ingredient_test_name)

        supplier_select = Select(
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, "suplier_choice"))
            )
        )
        supplier_select.select_by_visible_text(inventory_ingredient_test_supplier)

        inventory_ingredient_test_unit_cost_input = self.browser.find_element_by_id('ing-cost')
        inventory_ingredient_test_unit_cost_input.clear()
        inventory_ingredient_test_unit_cost_input.send_keys(inventory_ingredient_test_unit_cost)

        inventory_ingredient_test_unit_weight_input = self.browser.find_element_by_id('ing-weight')
        inventory_ingredient_test_unit_weight_input.clear()
        inventory_ingredient_test_unit_weight_input.send_keys(inventory_ingredient_test_unit_weight)

        inventory_ingredient_test_unit_current_stock_input = self.browser.find_element_by_id('ing-stock')
        inventory_ingredient_test_unit_current_stock_input.clear()
        inventory_ingredient_test_unit_current_stock_input.send_keys(inventory_ingredient_test_unit_current_stock)

        inventory_ingredient_test_minimum_stock_needed_input = self.browser.find_element_by_id('ing-stock-needed')
        inventory_ingredient_test_minimum_stock_needed_input.clear()
        inventory_ingredient_test_minimum_stock_needed_input.send_keys(inventory_ingredient_test_minimum_stock_needed) 
        

        save_changes_button = self.browser.find_element_by_id('update-inventory-ingredient-btn')
        save_changes_button.click()

        inventory_ingredient_rows = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")

        self.assertEquals(inventory_ingredient_rows[0].text, inventory_ingredient_test_name)
        self.assertEquals(inventory_ingredient_rows[1].text, inventory_ingredient_test_supplier)
        self.assertEquals(inventory_ingredient_rows[2].text, inventory_ingredient_test_unit_cost)
        self.assertEquals(inventory_ingredient_rows[3].text, inventory_ingredient_test_unit_weight)
        self.assertEquals(inventory_ingredient_rows[4].text, inventory_ingredient_test_unit_current_stock)
        self.assertEquals(inventory_ingredient_rows[5].text, inventory_ingredient_test_minimum_stock_needed)

    def test_delete_inventory_ingredient(self):

        inventory_ingredient_to_delete = str(1)

        inventory_ingredient_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")
        inventory_ingredient_name_before_deleting = inventory_ingredient_row[0].text 

        inventory_ingredient_edit_button = self.browser.find_elements_by_css_selector("button[data-id='"+inventory_ingredient_to_delete+"']")
        inventory_ingredient_edit_button[1].click()

        time.sleep(2)


        ingredient_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")

        self.assertNotEquals(ingredient_row[0].text, inventory_ingredient_name_before_deleting)

    def test_create_inventory_ingredient(self):

        inventory_ingredient_test_name = 'Test Inventory Ingredient'
        inventory_ingredient_test_supplier = 'Baker House'
        inventory_ingredient_test_unit_cost = '1.00'
        inventory_ingredient_test_unit_weight = '1.000'
        inventory_ingredient_test_unit_current_stock = '1.000'
        inventory_ingredient_test_minimum_stock_needed = '1.00'

        create_ingredient_button = self.browser.find_element_by_id('creat-inventory-ingredient')
        create_ingredient_button.click()

        time.sleep(2)
        inventory_ingredient_name_input = self.browser.find_element_by_id('ing-name-crt')
        inventory_ingredient_name_input.send_keys(inventory_ingredient_test_name)

        supplier_select = Select(
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, "suplier_choice_crt"))
            )
        )
        supplier_select.select_by_visible_text(inventory_ingredient_test_supplier)

        inventory_ingredient_test_unit_cost_input = self.browser.find_element_by_id('ing-cost-crt')
        inventory_ingredient_test_unit_cost_input.send_keys(inventory_ingredient_test_unit_cost)

        inventory_ingredient_test_unit_weight_input = self.browser.find_element_by_id('ing-weight-crt')
        inventory_ingredient_test_unit_weight_input.send_keys(inventory_ingredient_test_unit_weight)

        inventory_ingredient_test_unit_current_stock_input = self.browser.find_element_by_id('ing-stock-crt')
        inventory_ingredient_test_unit_current_stock_input.send_keys(inventory_ingredient_test_unit_current_stock)

        inventory_ingredient_test_minimum_stock_needed_input = self.browser.find_element_by_id('ing-stock-needed-crt')
        inventory_ingredient_test_minimum_stock_needed_input.send_keys(inventory_ingredient_test_minimum_stock_needed)

        create_inventory_ingredient_button = self.browser.find_element_by_id('create-inventory-ingredient-btn')
        create_inventory_ingredient_button.click()

        

        all_rows = self.browser.find_elements_by_xpath("//table/tbody/tr")
        number_of_rows = str(len(all_rows))

        inventory_ingredient_rows = self.browser.find_elements_by_xpath(
            "//table/tbody/tr["+number_of_rows+"]/td"
        )

        self.assertEquals(inventory_ingredient_rows[0].text, inventory_ingredient_test_name)
        self.assertEquals(inventory_ingredient_rows[1].text, inventory_ingredient_test_supplier)
        self.assertEquals(inventory_ingredient_rows[2].text, inventory_ingredient_test_unit_cost)
        self.assertEquals(inventory_ingredient_rows[3].text, inventory_ingredient_test_unit_weight)
        self.assertEquals(inventory_ingredient_rows[4].text, inventory_ingredient_test_unit_current_stock)
        self.assertEquals(inventory_ingredient_rows[5].text, inventory_ingredient_test_minimum_stock_needed)
        self.assertEquals(inventory_ingredient_rows[6].text, 'False')
