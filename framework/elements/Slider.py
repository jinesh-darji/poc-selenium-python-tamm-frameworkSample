from selenium.webdriver import ActionChains

from framework.browser.Browser import Browser
from framework.elements.base.BaseElement import BaseElement


class Slider(BaseElement):

    def __init__(self, locator_reader, element_key):
        super(Slider, self).__init__(locator_reader, element_key)

    def is_value_from_app_in_range_slider_data(self, app_locator, min_slider, max_slider):
        if int(app_locator) in range(int(min_slider), int(max_slider) + 1):
            return True
        else:
            return False

    def get_element_type(self):
        return "Slider"

    def get_slider_value(self):
        value = self.get_elements_text()
        return value

    def click_on_slider(self, step):
        en = self.find_element()
        move = ActionChains(Browser.get_driver())
        move.click_and_hold(en).move_by_offset(step, 0).release().perform()
