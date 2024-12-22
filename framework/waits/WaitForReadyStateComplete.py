from selenium.common.exceptions import StaleElementReferenceException

from framework.scripts import ScriptsJs


class WaitForReadyStateComplete(object):
    def __init__(self, browser):
        self.browser = browser

    def __call__(self, driver):
        try:
            self.browser.execute_script(ScriptsJs.SEND_JQUERY)
            return self.browser.execute_script(ScriptsJs.GET_PAGE_READY_STATE) == True
        except StaleElementReferenceException:
            return False
