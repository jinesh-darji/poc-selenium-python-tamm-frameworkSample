from framework.elements.base.BaseElement import BaseElement


class Button(BaseElement):

    def __init__(self, locator_reader, element_key):
        super(Button, self).__init__(locator_reader, element_key)

    def get_element_type(self):
        return "Button"

    def is_button_primary(self):
        return "uil-button_primary" in self.get_attribute("class")

    def is_button_secondary(self):
        return "uil-button_secondary" in self.get_attribute("class")

    def is_button_text(self):
        return "uil-button_text" in self.get_attribute("class")

    def is_button_text_secondary(self):
        return "uil-button_text_secondary" in self.get_attribute("class")

    def is_button_print(self):
        return "uil-button_secondary uil-button_icon-left" in self.get_attribute("class")

    def is_button_default(self):
        return "uil-button_default-appearance uil-button_primary" in self.get_attribute("class")

    def is_button_disabled(self):
        return self.get_elements()[1].get_attribute("disabled")
