from framework.elements.base.BaseElement import BaseElement


class Link(BaseElement):

    def __init__(self, locator_reader, element_key):
        super(Link, self).__init__(locator_reader, element_key)

    def get_element_type(self):
        return "Link"

    def get_href(self):
        return super(Link, self).get_attribute("href")
