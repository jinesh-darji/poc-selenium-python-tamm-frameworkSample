from axe_selenium_python import Axe

from framework.browser.Browser import Browser


class AccessibilityUtil:
    __axe = Axe(Browser.get_driver())
    __is_accessibility_failed = False

    @staticmethod
    def get_accessibility_check_result():
        AccessibilityUtil.__axe = Axe(Browser.get_driver())
        AccessibilityUtil.__axe.inject()
        results = AccessibilityUtil.__axe.execute()
        return len(results["violations"]) == 0, AccessibilityUtil.__axe.report(results["violations"])

    @staticmethod
    def set_accessibility_fail():
        AccessibilityUtil.__is_accessibility_failed = True

    @staticmethod
    def get_accessibility_fail():
        return AccessibilityUtil.__is_accessibility_failed
