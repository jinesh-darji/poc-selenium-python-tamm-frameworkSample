import logging
import random
import time

from selenium.webdriver.common.keys import Keys

from framework.browser.Browser import Browser
from framework.configuration import config
from framework.scripts import ScriptsJs
from framework.utils.StringUtil import StringUtil
from framework.utils.WaiterUtil import WaiterUtil
from framework.waits.WaitForReadyStateComplete import WaitForReadyStateComplete
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseElement(object):
    coordinate_x = 'x'
    coordinate_y = 'y'

    def __init__(self, locator_reader, element_key):
        self.__unformatted_name, self.__unformatted_locator, self.__search_condition = locator_reader.read_locator(
            element_key)
        self.__locator = self.__unformatted_locator
        self.__name = self.__unformatted_name

    def __getitem__(self, key):
        if (self.__search_condition != By.XPATH):
            raise TypeError("__getitem__ for BaseElement possible only when __search_condition == By.XPATH")
        else:
            return BaseElement(By.XPATH, self.__locator + "[" + str(key) + "]", self.__name)

    def try_wait_for_absent(self):
        def func():
            if self.is_present():
                raise StaleElementReferenceException()
            return True

        return self.try_until_not_stale(func, skip_exception=True)

    def format(self, *args):
        self.__name = self.__unformatted_name.format(*args)
        self.__locator = self.__unformatted_locator.format(*args)
        return self

    def get_locator(self):
        return self.__locator

    def get_search_condition(self):
        return self.__search_condition

    def get_name(self):
        return self.__name

    def wait_until_location_stable(self):
        def func():
            first_location = self.get_location()
            time.sleep(0.5)
            second_location = self.get_location()

            return first_location == second_location

        self.wait_for(func)

    def find_element(self):
        element = self.wait_for_check_by_condition(method_to_check=EC.presence_of_element_located,
                                                   message=" was not found")
        return element

    @staticmethod
    def get_displayed_elements(condition, locator):
        element_size = len(Browser.get_driver().find_elements(condition, locator))
        result_elements = []
        try:
            for ele_number in range(1, element_size + 1):
                element_locator = "({locator})[{number}]".format(locator=locator, number=ele_number)
                logging.info("Element searching with locator " + element_locator)
                element = WebDriverWait(Browser.get_driver(), config.EXPLICITLY_WAIT_SEC).until(
                    EC.visibility_of_element_located((condition, element_locator)))
                result_elements.append(element)
        except TimeoutException:
            error_msg = "element with locator was not found"
            logging.error(error_msg)
            raise TimeoutException(error_msg)
        return result_elements

    def is_enabled(self):
        def func():
            return self.find_element().is_enabled()

        return self.try_until_not_stale(func)

    def is_disabled(self):
        def func():
            return self.find_element().is_disabled()

        return self.try_until_not_stale(func)

    def is_selected(self):
        def func():
            return self.find_element().is_selected()

        return self.try_until_not_stale(func)

    def is_displayed(self):
        def func():
            return self.find_element().is_displayed()

        return self.try_until_not_stale(func)

    def is_present(self):
        return self.get_elements_count() > 0

    def is_visible(self):
        return self.is_displayed()

    def get_elements_count(self):
        elements_count = len(self.get_elements())
        return elements_count

    def get_elements(self):
        def func():
            return Browser.get_driver().find_elements(self.__search_condition, self.__locator)

        Browser.wait_for_page_to_load()
        Browser.set_implicit_wait(config.IS_PRESENT_IMPLICITLY_WAIT_SEC)
        elements = self.try_until_not_stale(func)
        Browser.set_implicit_wait()
        return elements

    def get_elements_text(self):
        return [elem.text for elem in self.get_elements()]

    def get_element_contains_text(self, text):
        for elem in self.get_elements():
            if text in elem.text:
                return elem

    def get_displayed_element(self):
        elements = self.get_elements()
        for element in elements:
            if element.is_displayed():
                return element

    @staticmethod
    def get_text_of_inner_element(e):
        html = e.get_attribute('innerHTML')
        return html

    def send_keys(self, key):
        logging.info("send_keys: Change element text '" + self.get_name() + "' to => '" + key + "'")

        def func(key):
            self.find_element().send_keys(key)
            return True

        self.wait_for(func, key)

    def click(self):
        logging.info("click: Click by element '" + self.get_name() + "'")

        def func():
            self.find_element().click()
            return True

        self.wait_for(func)

    def click_js(self):
        logging.info("click: Click by element via JS '" + self.get_name() + "'")

        def func():
            Browser.execute_script(ScriptsJs.CLICK, self.find_element())
            return True

        self.wait_for(func)

    def get_text(self):
        logging.info("get_text: Get element text '" + self.get_name() + "'")

        def func():
            return self.find_element().text

        return self.wait_for(func)

    def get_text_content(self):
        def func():
            return Browser.get_driver().execute_script("return arguments[0].textContent;", self.find_element())

        return self.wait_for(func)

    def get_class(self):
        return self.get_attribute("class")

    def get_value(self):
        return self.get_attribute("value")

    def is_element_disabled(self):
        try:
            return self.get_attribute("disabled") == "true"
        except TimeoutException:
            return False

    def get_attribute(self, attr):
        logging.info("get_attribute: " + attr + " for element '" + self.get_name() + "'")

        def func(attr):
            return self.find_element().get_attribute(name=attr)

        return self.wait_for(func, attr)

    def get_attribute_list(self, attr):
        logging.info("get_attribute list: " + attr + " for element '" + self.get_name() + "'")

        def func(attr):
            return [elem.get_attribute(name=attr) for elem in self.get_elements()]

        return self.wait_for(func, attr)

    def get_attribute_class(self):
        return self.get_attribute("class")

    def scroll_by_script(self):
        self.wait_for_is_present()
        logging.info("Scroll to element '" + self.get_name() + "'")

        def func():
            return Browser.execute_script(ScriptsJs.SCROLL_INTO_VIEW, self.find_element())

        self.wait_for(func)

    def double_click(self):
        self.wait_for_is_present()
        logging.info("double_click: Double click by element '" + self.get_name() + "'")

        def func():
            ActionChains(Browser.get_driver()).double_click(self.find_element()).perform()

        self.wait_for(func)

    def right_click(self):
        self.wait_for_is_present()
        logging.info("right_click: Right click by element '" + self.get_name() + "'")

        def func():
            ActionChains(Browser.get_driver()).context_click(self.find_element()).perform()

        self.wait_for(func)

    def move_to_element(self):
        self.wait_for_is_present()
        logging.info("double_click: Double click by element '" + self.get_name() + "'")

        def func():
            ActionChains(Browser.get_driver()).move_to_element(self.find_element()).perform()

        self.wait_for(func)

    def wait_for_is_present(self):
        self.wait_for_check_by_condition(method_to_check=EC.presence_of_element_located,
                                         message=" doesn't exist")

    def wait_for_is_displayed(self):
        WaiterUtil.wait_for_true(self.is_displayed)

    def wait_for_is_absent(self):
        self.wait_for_check_by_condition(method_to_check=EC.invisibility_of_element_located,
                                         message=" already exists")

    def wait_for_element_disappear(self):
        def func():
            return len(self.get_elements()) == 0

        self.wait_for(func)

    def wait_for_text(self, text):
        def func(text):
            return text in self.find_element().text

        self.wait_for(func, text)

    def wait_for_value(self, text):
        def func(text):
            return text in self.get_attribute("value")

        self.wait_for(func, text)

    def wait_for_visibility(self):
        self.wait_for(self.is_visible())

    def wait_for_check_by_condition(self, method_to_check, message, wait_time_sec=config.EXPLICITLY_WAIT_SEC,
                                    use_default_msg=True):
        try:
            element = WebDriverWait(Browser.get_driver(),
                                    wait_time_sec,
                                    ignored_exceptions=[StaleElementReferenceException]). \
                until(method=method_to_check((self.get_search_condition(), self.get_locator())))
        except TimeoutException:
            result_message = ("Element '" + self.get_name() + "' with locator" + self.get_locator() + message
                              if use_default_msg else message)
            logging.warning(result_message)
            raise TimeoutException(result_message)
        return element

    def get_location(self):
        def func():
            return self.find_element().location

        return self.wait_for(func)

    def get_location_vertical(self):
        def func():
            return self.find_element().location[BaseElement.coordinate_y]

        return self.wait_for(func)

    def get_location_horizontal(self):
        def func():
            return self.find_element().location[BaseElement.coordinate_x]

        return self.wait_for(func)

    @staticmethod
    def get_list_of_elements_vertical_locations(condition, locator):
        other_elements = BaseElement.get_displayed_elements(condition, locator)
        return [element.location[BaseElement.coordinate_y] for element in other_elements]

    @staticmethod
    def get_dict_of_elements_vertical_locations_and_text(condition, locator):
        events_time_elements = BaseElement.get_displayed_elements(condition, locator)
        events_info = {}
        for element in events_time_elements:
            events_info[element.location[BaseElement.coordinate_y]] = element.text
        return events_info

    def wait_for(self, condition, *args, **kwargs):
        def func(driver):
            try:
                WaitForReadyStateComplete(Browser)(driver)
                value = condition(*args, **kwargs)
                return value
            except StaleElementReferenceException:
                return False

        return WebDriverWait(Browser.get_driver(),
                             config.EXPLICITLY_WAIT_SEC,
                             ignored_exceptions=[StaleElementReferenceException]).until(func)

    def try_until_not_stale(self, method, skip_exception=False, *args, **kwargs):
        return Browser.try_until_not_exceptions((StaleElementReferenceException,), method,
                                                config.EXPLICITLY_WAIT_SEC, config.CUSTOM_WAIT_STEPTIME,
                                                skip_exception=skip_exception, *args, **kwargs)

    def wait_for_elements_count_present(self, count):
        def func():
            return self.get_elements_count() == count

        self.wait_for(func)

    def get_random_element(self):
        element_count = self.get_elements_count()
        index = random.randint(0, element_count - 1)
        return self.get_elements()[index]

    def wait_for_list_is_not_empty(self):
        def func():
            return len(self.get_elements_text()) > 0

        self.wait_for(func)

    def get_random_items_from_list(self, items_count):
        self.wait_until_location_stable()
        self.wait_for_list_is_not_empty()

        data_list = self.get_elements_text()
        if items_count == 1:
            return random.choice(data_list)
        else:
            result = [random.choice(data_list)]
            for i in range(items_count - 1):
                result.append(random.choice(data_list))
                item = result[i + 1]
                while result.count(item) > 1:
                    del result[i + 1]
                    result.append(random.choice(data_list))
            return result

    def get_list_of_digits(self):
        self.wait_until_location_stable()
        self.wait_for_list_is_not_empty()

        list_of_digits = []
        data_list = self.get_elements_text()
        for i in data_list:
            list_of_digits.append(int(StringUtil.get_text_only_digits(i)))
        return list_of_digits

    def get_width_js(self):
        return Browser.execute_script(ScriptsJs.GET_WIDTH, self.find_element())

    def click_enter_button(self):
        self.send_keys(Keys.ENTER)