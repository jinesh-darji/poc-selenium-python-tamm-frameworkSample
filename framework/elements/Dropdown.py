from framework.elements.Label import Label
from framework.elements.base.BaseElement import BaseElement


class Dropdown(BaseElement):

    def __init__(self, locator_reader, element_key, arrow_key):
        super(Dropdown, self).__init__(locator_reader, element_key)
        self.dropdown_arrow = Label(locator_reader, arrow_key)

    def get_element_type(self):
        return "Dropdown"

    def open_dropdown(self):
        self.dropdown_arrow.wait_until_location_stable()
        self.dropdown_arrow.scroll_by_script()
        self.dropdown_arrow.click()

    def return_and_click_random_data_drpdwn(self, dropdown_locator, item_locator, dropdown_list):
        """
        Method connected with clicking and inputting data in drop-down and returning selected item
        :return: str: selected value from drop down
        """
        dropdown_locator.wait_until_location_stable()
        dropdown_locator.open_dropdown()
        dropdown_list.wait_until_location_stable()
        data = dropdown_list.get_random_items_from_list(1)
        item_locator.format(data).click_js()  # confirmed by customer
        return data

    @staticmethod
    def get_and_click_upper_case_item(drpdwn_locator, drpdwn_item, drpdwn_list):
        """
        Method connected with selecting random data from drop-down and returning value
        :return: str: selected value from drop down
        """
        return drpdwn_locator.return_and_click_random_data_drpdwn(drpdwn_locator, drpdwn_item, drpdwn_list).upper()

    @staticmethod
    def get_list_of_visible_drpdwn_values(min_value, max_value):
        """
        Method connected with getting list with min and max data from drop-downs
        :return: list: list with min and max data
        """
        list_dropdown = [min_value, max_value]
        return list_dropdown

    def return_and_click_specific_data_drpdwn(self, dropdown_locator, item_locator, data):
        """
        Method connected with clicking and inputting data in drop-down and returning selected item
        :return: str: selected value from drop down
        """
        dropdown_locator.open_dropdown()
        item_locator.format(data)
        item_locator.wait_until_location_stable()
        item_locator.click()
        return data

    @staticmethod
    def get_specific_item_from_dropdown(drpdwn_locator, drpdwn_item, data):
        """
        Method connected with selecting specific data from drop-down and returning value
        :return: str: selected value from drop down
        """
        return drpdwn_locator.return_and_click_specific_data_drpdwn(drpdwn_locator, drpdwn_item, data).upper()
