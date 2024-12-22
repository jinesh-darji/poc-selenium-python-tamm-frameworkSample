from framework.elements.base.BaseElement import BaseElement


class Checkbox(BaseElement):

    def __init__(self, locator_reader, element_key):
        super(Checkbox, self).__init__(locator_reader, element_key)

    def get_element_type(self):
        return "Checkbox"

    def is_checkbox_selected(self):
        """
        Method connected with selection Villa checkbox on Filter Form
        """
        self.wait_until_location_stable()
        return self.is_selected()
