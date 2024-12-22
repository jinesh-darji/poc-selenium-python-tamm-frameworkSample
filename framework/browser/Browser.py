import inspect
import logging
import time

from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from framework.browser.BrowserFactory import BrowserFactory
from framework.configuration import config
from framework.scripts import ScriptsJs
from framework.waits.WaitForReadyStateComplete import WaitForReadyStateComplete


class Browser:
    __web_driver = None
    __main_window_handle = None
    __is_accessibility_failed = False
    __axe = None
    __verification_errors = []

    @staticmethod
    def get_driver():
        return Browser.__web_driver

    @staticmethod
    def set_up_driver(capabilities=None, is_incognito=False):
        logging.info('Driver initialization for browser ' + config.BROWSER)
        Browser.__web_driver = BrowserFactory.get_browser_driver(capabilities=capabilities,
                                                                 is_incognito=is_incognito)
        Browser.__web_driver.implicitly_wait(config.IMPLICITLY_WAIT_SEC)
        Browser.__web_driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT_SEC)
        Browser.__web_driver.set_script_timeout(config.SCRIPT_TIMEOUT_SEC)
        Browser.__main_window_handle = Browser.get_driver().current_window_handle

    @staticmethod
    def quit():
        if Browser.__web_driver is not None:
            logging.info("Quiting driver")
            Browser.__web_driver.quit()
            Browser.__web_driver = None

    @staticmethod
    def close(page_name=""):
        if Browser.get_driver() is not None:
            logging.info("Closing page %s " % page_name)
            Browser.get_driver().close()

    @staticmethod
    def refresh_page():
        logging.info("Refreshing page")
        Browser.get_driver().refresh()

    @staticmethod
    def maximize():
        Browser.__web_driver.maximize_window()

    @staticmethod
    def set_url(url):
        logging.info("Changing url to " + url)
        Browser.get_driver().get(url)

    @staticmethod
    def execute_script(script, *arguments):
        result = Browser.get_driver().execute_script(script, *arguments)
        return result if result else True

    @staticmethod
    def get_current_url():
        return Browser.get_driver().current_url

    @staticmethod
    def back_page():
        Browser.get_driver().back()

    @staticmethod
    def wait_for_page_to_load():
        WebDriverWait(Browser.get_driver(), config.PAGE_LOAD_TIMEOUT_SEC).until(WaitForReadyStateComplete(Browser))

    @staticmethod
    def set_implicit_wait(wait_time_sec=config.IMPLICITLY_WAIT_SEC):
        Browser.get_driver().implicitly_wait(wait_time_sec)

    @staticmethod
    def is_correct_type(exceptions):
        is_correct_type = isinstance(exceptions, tuple)
        if not is_correct_type:
            if inspect.isclass(exceptions) and issubclass(exceptions, Exception):
                exceptions = (exceptions,)
                is_correct_type = True
            if isinstance(exceptions, list):
                exceptions = tuple(exceptions)
                is_correct_type = True
        return is_correct_type, exceptions

    @staticmethod
    def try_until_not_exceptions(exceptions, method, timeout, step_time, skip_exception=False, *args, **kwargs):
        end_time = time.time() + timeout
        is_correct_type, exceptions = Browser.is_correct_type(exceptions)
        if not is_correct_type:
            raise ValueError("exceptions must be tuple or list of Exception subclasses or Exception subclass")
        while time.time() <= end_time:
            try:
                value = method(*args, **kwargs)
                return value
            except exceptions:
                time.sleep(step_time)
                if time.time() > end_time:
                    break
        if not skip_exception:
            raise TimeoutException
        return False

    @staticmethod
    def get_accessibility_check_result():
        Browser.__axe.inject()
        results = Browser.__axe.execute()
        return len(results["violations"]) == 0, Browser.__axe.report(results["violations"])

    @staticmethod
    def scroll_to_top():
        Browser.execute_script(ScriptsJs.SCROLL_TO_TOP)

    @staticmethod
    def scroll_to_down():
        Browser.execute_script(ScriptsJs.SCROLL_TO_DOWN)

    @staticmethod
    def switch_main_window():
        logging.info("Swithch to the main window")
        try:
            Browser.get_driver().switch_to_window(Browser.__main_window_handle)
        except NoSuchWindowException:
            logging.info("The main window is absent")

    @staticmethod
    def switch_to_default_content():
        logging.info("Switch to the main frame")
        Browser.get_driver().switch_to.default_content()

    @staticmethod
    def frame_switch(name):
        Browser.get_driver().switch_to.frame(Browser.get_driver().find_element_by_xpath(name))

    @staticmethod
    def turn_off_implicit_wait():
        Browser.get_driver().implicitly_wait(0)

    @staticmethod
    def scroll_by_keys():
        Browser.get_driver().find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    @staticmethod
    def open_url_in_new_tab(url):
        Browser.get_driver().execute_script("window.open('{}')".format(url))

    @staticmethod
    def switch_to_tab(tab_index):
        Browser.get_driver().switch_to_window(Browser.get_driver().window_handles[tab_index])
