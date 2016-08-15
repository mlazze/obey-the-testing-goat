from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from functional_tests.base import FunctionalTest
from functional_tests.home_and_list_pages import HomePage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))
        oni_browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                       desired_capabilities=DesiredCapabilities.CHROME)
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        self.browser = edith_browser
        list_page = HomePage(self).start_new_list('Get help')

        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@example.com')

        list_page.share_list_with('oniciferous@example.com')

        self.browser = oni_browser

        HomePage(self).go_to_home_page().go_to_my_lists_page()

        self.browser.find_element_by_link_text('Get help').click()

        self.wait_for(lambda: self.assertEqual(list_page.get_list_owner(), 'edith@example.com'))
        list_page.add_new_item('Hi Edith!')

        self.browser = edith_browser
        self.browser.refresh()

        list_page.wait_for_new_item_in_list('Hi Edith!', 2)
