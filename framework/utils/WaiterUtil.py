import logging
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from framework.browser.Browser import Browser
from framework.configuration import config
from framework.waits.WaitForTrue import WaitForTrue


class WaiterUtil:
    @staticmethod
    def wait_for_true(expression, time_in_seconds=config.IMPLICITLY_WAIT_SEC, msg=""):
        try:
            return WebDriverWait(Browser.get_driver(), time_in_seconds).until(WaitForTrue(Browser, expression))
        except TimeoutException:
            error_msg = "After {time} seconds not executed event: {msg}".format(time=time_in_seconds,
                                                                                msg=msg)
            logging.warning(error_msg)
            raise TimeoutException(error_msg)

    @staticmethod
    def wait_for_time(start_time, msg=""):
        end_time = start_time + config.CYCLE_WAIT_TIMEOUT
        result = time.time() <= end_time
        if result:
            return result
        raise TimeoutError(msg=msg)