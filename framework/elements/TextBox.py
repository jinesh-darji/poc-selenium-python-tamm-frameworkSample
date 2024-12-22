from selenium.webdriver.common.keys import Keys

from framework.elements.base.BaseElement import BaseElement


class TextBox(BaseElement):
    def __init__(self, locator_reader, element_key):
        super(TextBox, self).__init__(locator_reader, element_key)

    test_input = "test form"

    def get_element_type(self):
        return "TextBox"

    def get_value(self):
        return super(TextBox, self).get_attribute("value")

    def clear_field(self):
        self.send_keys(Keys.CONTROL + 'a')
        self.send_keys(Keys.DELETE)

    def is_text_box_success(self):
        return 'has-success' in self.get_attribute("class")

    def is_text_box_failure(self):
        return 'has-error' in self.get_attribute("class")

    def is_text_box_disabled(self):
        return 'input_disabled' in self.get_attribute("class")

    def set_input_value(self):
        self.send_keys(self.test_input)
        return self.get_attribute("value") == self.test_input
