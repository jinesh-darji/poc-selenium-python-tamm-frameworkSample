from selenium.webdriver.common.keys import Keys

from framework.browser.Browser import Browser
from framework.configuration import config
from framework.constants import Browsers
from framework.elements.Label import Label
from framework.elements.TextBox import TextBox
from framework.elements.base.BaseElement import BaseElement


class InputDropdown(BaseElement):

    def __init__(self, locator_reader, element_key, arrow_key, txb_key):
        super(InputDropdown, self).__init__(locator_reader, element_key)
        self.dropdown_arrow = Label(locator_reader, arrow_key)
        self.dropdown_txb = TextBox(locator_reader, txb_key)

    def get_element_type(self):
        return "InputDropdown"

    def open_dropdown(self):
        self.dropdown_arrow.wait_until_location_stable()
        self.dropdown_arrow.click()
        if config.BROWSER == Browsers.BROWSER_ANDROID or config.BROWSER == Browsers.BROWSER_IOS:
            Browser.get_driver().hide_keyboard()

    def select_value(self, value):
        self.dropdown_txb.send_keys(value)
        self.dropdown_txb.send_keys(Keys.ENTER)
