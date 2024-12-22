from framework.elements.base.BaseElement import BaseElement


class List(BaseElement):

    def __init__(self, locator_reader, element_key):
        super(List, self).__init__(locator_reader, element_key)

    def get_element_type(self):
        return "List"
