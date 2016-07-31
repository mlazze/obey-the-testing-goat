import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return

        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                        desired_capabilities=DesiredCapabilities.CHROME)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        text1 = 'Buy peacock feathers'
        input_box.send_keys(text1)
        input_box.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, r'/lists/.+')

        self.check_for_row_in_list_table('1: ' + text1)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        text2 = 'Use peacock feathers to make a fly'
        input_box.send_keys(text2)
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: ' + text2)

        self.browser.quit()
        self.browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                        desired_capabilities=DesiredCapabilities.CHROME)

        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(text1, page_text)
        self.assertNotIn('make a fly', page_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        text3 = 'Buy milk'
        input_box.send_keys(text3)
        input_box.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, r'/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(text1, page_text)
        self.assertIn(text3, page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size['width'] / 2, 512, delta=10)
        inputbox.send_keys('testing\n')
        self.browser.find_element_by_id('id_new_item')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size['width'] / 2, 512, delta=10)
