import time
from decimal import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class EposTests(StaticLiveServerTestCase):

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

    def test_change_order_number(self):
        

        order_number = "44"

        order_number_button = self.browser.find_element_by_id('order-number-anchor')
        order_number_button.click()
        time.sleep(2)

        order_number_input = self.browser.find_element_by_id('order-number-input')
        time.sleep(2)
        order_number_input.send_keys(order_number)

        save_changes_button = self.browser.find_element_by_id('modal-order-number-button')
        save_changes_button.click()

        order_number_content = self.browser.find_element_by_class_name('order-number').text

        self.assertEquals(order_number, order_number_content)

    def test_change_order_type(self):

        order_type_1 = "Have In"
        order_type_2 = "Take Out"

        order_type_button = self.browser.find_element_by_id('order-type-anchor')
        time.sleep(2)
        order_type_button.click()

        order_type_1_button = self.browser.find_element_by_id('have-in')
        time.sleep(2)
        order_type_1_button.click()

        save_changes_button = self.browser.find_element_by_id('modal-order-type-button')
        time.sleep(2)
        save_changes_button.click()

        order_type_content = self.browser.find_element_by_class_name('order-type').text

        self.assertEquals(order_type_1, order_type_content)
        time.sleep(2)

        order_type_button.click()

        order_type_2_button = self.browser.find_element_by_id('take-out')

        time.sleep(1)
        order_type_2_button.click()
        time.sleep(1)
        save_changes_button.click()
        time.sleep(3)

        order_type_content = self.browser.find_element_by_class_name('order-type').text

        self.assertEquals(order_type_2, order_type_content)

    def test_place_an_order(self):
        time.sleep(2)
        
        products_to_order = ['Latte', 'Green Tea', 'Can Coke']
        products_to_order_category_ids = [8, 8, 9]
        products_to_order_times = [2,1,3]
        products_to_order_single_price = [2.60, 1.40, 2.00]
        tax = 0.10

        for i in range(0,len(products_to_order)):
            time.sleep(5)        
            product_category_button = self.browser.find_element_by_css_selector(
                "button[data-id='"+ str(products_to_order_category_ids[i])+"']"
            )
            product_category_button.click()

            time.sleep(5) 
            product_button = self.browser.find_element_by_css_selector(
                "button[data-name='"+products_to_order[i]+"']"
            )

            for j in range(0, products_to_order_times[i]):
                product_button.click()

        time.sleep(2)

        products_table_row_one = self.browser.find_elements_by_class_name('product-name')[0].text
        products_table_row_two = self.browser.find_elements_by_class_name('product-name')[1].text
        products_table_row_three = self.browser.find_elements_by_class_name('product-name')[2].text

        self.assertEqual(products_table_row_one, 'Latte')
        self.assertEqual(products_table_row_two, 'Green Tea')
        self.assertEqual(products_table_row_three, 'Can Coke')

        time.sleep(2)

        order_type_button = self.browser.find_element_by_id('order-type-anchor')
        time.sleep(2)
        order_type_button.click()

        order_type_1_button = self.browser.find_element_by_id('have-in')
        time.sleep(2)
        order_type_1_button.click()

        save_changes_button = self.browser.find_element_by_id('modal-order-type-button')
        time.sleep(2)
        save_changes_button.click()

        total_amount_before_tax = 0
        for i in range(len(products_to_order_single_price)):
            total_amount_before_tax += round(products_to_order_single_price[i]*products_to_order_times[i], 2)

        total_amount_after_tax = "%.2f"%(round((total_amount_before_tax*tax) + total_amount_before_tax,2))
        total_amount_before_tax = "%.2f"%total_amount_before_tax

        price_before_tax_label = self.browser.find_element_by_class_name('total-amount-row2')
        price_before_tax_label = price_before_tax_label.find_element_by_tag_name('span').text

        price_after_tax_label = self.browser.find_element_by_class_name('price-total')
        price_after_tax_label = price_after_tax_label.find_element_by_tag_name('span').text

        assert price_before_tax_label == total_amount_before_tax
        assert price_after_tax_label == price_after_tax_label


    def test_change_quantity_of_selected_product(self):

        product_button = self.browser.find_element_by_css_selector("button[data-name='Latte']")
        time.sleep(2)
        product_button.click()

        products_table_row = self.browser.find_elements_by_class_name('product-quantity')[0].text

        self.assertEqual(products_table_row, '1')

        add_button = self.browser.find_elements_by_class_name('fa-plus')[0]
        time.sleep(2)
        add_button.click()

        products_table_row = self.browser.find_elements_by_class_name('product-quantity')[0].text

        self.assertEqual(products_table_row,'2')

        remove_button = self.browser.find_elements_by_class_name('fa-minus')[0]
        time.sleep(2)
        remove_button.click()

        products_table_row = self.browser.find_elements_by_class_name('product-quantity')[0].text

        self.assertEqual(products_table_row, '1')

    def test_analytics(self):

        late = 13
        cappuchino = 4
        single_espresso = 5
        double_espresso = 12

        late_button = self.browser.find_element_by_css_selector("button[data-name='Latte']")
        for i in range(late):
            late_button.click()
        time.sleep(2)

        cappuchino_button = self.browser.find_element_by_css_selector("button[data-name='Cappuccino']")
        for i in range(cappuchino):
            cappuchino_button.click()
        time.sleep(2)

        signel_espresso_button = self.browser.find_element_by_css_selector("button[data-name='Single Espresso']")
        for i in range(single_espresso):
            signel_espresso_button.click()
        time.sleep(2)

        double_espresso_button = self.browser.find_element_by_css_selector("button[data-name='Double Espresso']")
        for i in range(double_espresso):
            double_espresso_button.click()
        time.sleep(2)

        pay_button = self.browser.find_element_by_class_name('pay-order-button')
        total_amount_text = pay_button.find_element_by_tag_name('span').text

        pay_button.click()
        time.sleep(2)

        cash_button = self.browser.find_element_by_id('1a')
        cash_button.click()
        
        time.sleep(2)
        self.browser.get(self.live_server_url + '/analytics/')
        time.sleep(2)

        today_revenue = self.browser.find_element_by_class_name('today-revenue-amount ').text

        self.assertEquals(total_amount_text, today_revenue[1:])

        time.sleep(2)

        top_10_sold_latte_label = self.browser.find_element_by_css_selector("td[data-name='Latte']").text 
        top_10_sold_latte_number_sold = self.browser.find_element_by_css_selector("td[data-name='Latte-count']").text 

        top_10_sold_double_espresso_label = self.browser.find_element_by_css_selector("td[data-name='Double Espresso']").text 
        top_10_sold_double_espresso_number_sold = self.browser.find_element_by_css_selector("td[data-name='Double Espresso-count']").text 

        top_10_sold_single_espresso_label = self.browser.find_element_by_css_selector("td[data-name='Single Espresso']").text 
        top_10_sold_single_espresso_number_sold = self.browser.find_element_by_css_selector("td[data-name='Single Espresso-count']").text 

        top_10_sold_cappuchino_label = self.browser.find_element_by_css_selector("td[data-name='Cappuccino']").text 
        top_10_sold_cappuchino_number_sold = self.browser.find_element_by_css_selector("td[data-name='Cappuccino-count']").text 
        

        self.assertEquals(top_10_sold_latte_label, "Latte")
        self.assertEquals(top_10_sold_double_espresso_label, "Double Espresso")
        self.assertEquals(top_10_sold_single_espresso_label, "Single Espresso")
        self.assertEquals(top_10_sold_cappuchino_label, "Cappuccino")

        self.assertEquals(top_10_sold_latte_number_sold, str(late))
        self.assertEquals(top_10_sold_double_espresso_number_sold, str(double_espresso))
        self.assertEquals( top_10_sold_single_espresso_number_sold, str(single_espresso))
        self.assertEquals(top_10_sold_cappuchino_number_sold, str(cappuchino))
