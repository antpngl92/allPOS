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
        self.browser.get(self.live_server_url+'/ingridients/')
        time.sleep(2)

    def tearDown(self):
        self.browser.quit()

    def test_edit_ingredient(self):

        ingredient_test_name = 'Test Ingredient'
        ingredient_test_quantity = '0.500'

        ingredient_to_edit = str(17)

        ingredient_edit_button = self.browser.find_elements_by_css_selector(
            "button[data-id='"+ingredient_to_edit+"']"
        )
        ingredient_edit_button[0].click()

        time.sleep(2)
        ingredient_name_input = self.browser.find_element_by_id('ing2-name')
        ingredient_name_input.clear()
        ingredient_name_input.send_keys(ingredient_test_name)

        ingredient_quantity_input = self.browser.find_element_by_id('ing-quant')
        ingredient_quantity_input.clear()
        ingredient_quantity_input.send_keys(ingredient_test_quantity)

        save_changes_button = self.browser.find_element_by_id('update-ingredient-btn')
        save_changes_button.click()

        ingredient_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")

        self.assertEquals(ingredient_row[0].text, ingredient_test_name)
        self.assertEquals(ingredient_row[1].text, ingredient_test_quantity)

    def test_delete_ingredient(self):

        ingredient_to_edit = str(17)

        ingredient_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")
        ingredient_name_before_deleting = ingredient_row[0].text

        ingredient_edit_button = self.browser.find_elements_by_css_selector(
            "button[data-id='"+ingredient_to_edit+"']"
        )
        ingredient_edit_button[1].click()

        time.sleep(2)
        ingredient_row = self.browser.find_elements_by_xpath("//table/tbody/tr[1]/td")
        time.sleep(2)

        self.assertNotEquals(ingredient_row[0].text, ingredient_name_before_deleting)

    def test_create_ingredient(self):

        ingredient_test_name = 'Test Ingredient'
        ingredient_test_quantity = '0.500'
        ingredient_test_rii = 'Eggs 30pc.'

        create_ingredient_button = self.browser.find_element_by_id('creat-ingredient')
        create_ingredient_button.click()

        time.sleep(2)
        ingredient_name_input = self.browser.find_element_by_id('ing2-name')
        ingredient_name_input.send_keys(ingredient_test_name)

        ingredient_quantity_input = self.browser.find_element_by_id('ing-quant')
        ingredient_quantity_input.send_keys(ingredient_test_quantity)

        select = Select(
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, "related-inventory-ingredient-choice"))
            )
        )
        select.select_by_visible_text(ingredient_test_rii)

        ingredient_edit_button = self.browser.find_elements_by_css_selector(
            "button[id='create-ingredient-btn']"
        )
        ingredient_edit_button[0].click()
        time.sleep(2)

        all_rows = self.browser.find_elements_by_xpath("//table/tbody/tr")
        number_of_rows = str(len(all_rows))

        ingredient_row = self.browser.find_elements_by_xpath(
            "//table/tbody/tr["+number_of_rows+"]/td"
        )

        self.assertEquals(ingredient_row[0].text, ingredient_test_name)
        self.assertEquals(ingredient_row[1].text, ingredient_test_quantity)
        self.assertEquals(ingredient_row[2].text, ingredient_test_rii)
