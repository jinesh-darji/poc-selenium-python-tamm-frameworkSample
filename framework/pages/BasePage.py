import allure
from _pytest.outcomes import Failed
from allure import MASTER_HELPER as ALLURE_HELPER
from allure.common import StepContext
from allure.structure import TestStep, TestCase
from allure.utils import now
from selenium.common.exceptions import TimeoutException

from framework.browser.Browser import Browser
from framework.configuration import config
from framework.scripts import ScriptsJs
from framework.utils.AccessibilityUtil import AccessibilityUtil
from framework.utils.SoftAssert import SoftAssert


class BasePage:
    def __init__(self, element):
        self.page_element = element
        self.wait_page_to_load()
        self._do_accessibility_check()

    def wait_page_to_load(self):
        Browser.wait_for_page_to_load()

    def is_opened(self):
        self.wait_page_to_load()
        try:
            self.page_element.wait_for_is_present()
        except TimeoutException:
            return False
        return True

    def wait_for_page_closed(self):
        self.wait_page_to_load()
        self.page_element.wait_for_is_absent()

    def wait_for_page_opened(self):
        self.wait_page_to_load()
        self.page_element.wait_for_is_present()

    def allure_accessibility(self):
        step_name = "Accessibility_check_{}".format(self.page_element.get_name())
        step_context = StepContext(ALLURE_HELPER._allurelistener, step_name)
        step_context.step = TestStep(name=step_name, title=step_name, start=now(), attachments=[], steps=[])
        allure_stack = ALLURE_HELPER._allurelistener.stack
        for i in range(len(allure_stack) - 1, -1, -1):
            if isinstance(allure_stack[i], TestCase):
                allure_stack[i].steps.append(step_context.step)
                break
        allure_stack.append(step_context.step)
        result, data = AccessibilityUtil.get_accessibility_check_result()
        if result:
            step_context.__exit__(None, None, None)
        else:
            allure.attach("Report", data)
            step_context.__exit__(Failed, None, None)
            AccessibilityUtil.set_accessibility_fail()

    def _do_accessibility_check(self):
        if config.CHECK_ACCESSIBILITY:
            if ALLURE_HELPER._allurelistener:
                self.allure_accessibility()
            else:
                result, data = AccessibilityUtil.get_accessibility_check_result()
                SoftAssert.soft_assert(result,
                                       "\n Accessibility for " + self.page_element.get_name() + " failed: " + data)
            Browser.scroll_to_top()

    def scroll_to_element(self, element):
        Browser.execute_script(ScriptsJs.SCROLL_INTO_PAGE, self.page_element.find_element(), element.find_element())

    def scroll_to_top(self):
        Browser.scroll_to_top()
