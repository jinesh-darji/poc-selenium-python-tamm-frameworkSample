from selenium.common.exceptions import TimeoutException


class BaseForm:
    def __init__(self, element):
        self.form_element = element

    def is_opened(self):
        try:
            self.form_element.wait_for_is_present()
        except TimeoutException:
            return False
        return True

    def wait_for_form_closed(self):
        self.form_element.wait_for_is_absent()

    def wait_for_form_opened(self):
        self.form_element.wait_for_is_present()
