from unittest import skip

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Buy Milk\n')
        self.check_for_row_in_list_table('1: Buy Milk')

        self.get_item_input_box().send_keys('\n')
        self.check_for_row_in_list_table('1: Buy Milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy Milk')
        self.check_for_row_in_list_table('2: Make tea')
