from appium import webdriver as appiumdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from framework.configuration import config
from framework.constants import Browsers


class BrowserFactory:

    @staticmethod
    def get_browser_driver(capabilities=None, is_incognito=False):
        chrome_options = webdriver.ChromeOptions()
        firefox_profile = webdriver.FirefoxProfile()

        if config.HEADLESS == "y":
            chrome_options.add_argument("--headless")
        if is_incognito:
            chrome_options.add_argument("--incognito")
            firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

        if capabilities is None:
            capabilities = {}
        if config.USE_SELENOID:
            if config.BROWSER == Browsers.BROWSER_CHROME:
                return BrowserFactory.get_remote_driver(browser_name=config.BROWSER,
                                                        browser_version=config.CHROME_VERSION,
                                                        options=chrome_options, capabilities=capabilities)
            elif config.BROWSER == Browsers.BROWSER_FIREFOX:
                return BrowserFactory.get_remote_driver(browser_name=config.BROWSER,
                                                        browser_version=config.FIREFOX_VERSION,
                                                        browser_profile=firefox_profile, capabilities=capabilities)
        else:
            if config.BROWSER == Browsers.BROWSER_CHROME:
                return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                                        desired_capabilities=capabilities)
            elif config.BROWSER == Browsers.BROWSER_FIREFOX:
                return webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                         firefox_profile=firefox_profile,
                                         desired_capabilities=capabilities)

            elif config.BROWSER == Browsers.BROWSER_SAFARI:
                return webdriver.Safari(desired_capabilities=capabilities)
            elif config.BROWSER == Browsers.BROWSER_IOS:
                return BrowserFactory.get_ios_driver(capabilities)
            elif config.BROWSER == Browsers.BROWSER_ANDROID:
                return BrowserFactory.get_android_driver(capabilities)

    @staticmethod
    def get_ios_driver(capabilities):
        capabilities["browserName"] = Browsers.BROWSER_SAFARI
        if config.MOBILE_UDID:
            capabilities["startIWDP"] = True
        return BrowserFactory.get_appium_driver(capabilities)

    @staticmethod
    def get_android_driver(capabilities):
        capabilities["avd"] = config.MOBILE_DEVICE_NAME
        capabilities["browserName"] = Browsers.BROWSER_CHROME
        capabilities["forceMjsonwp"] = True
        if config.MOBILE_CHROMEDRIVER_VERSION:
            capabilities["chromedriverExecutable"] = ChromeDriverManager(
                version=config.MOBILE_CHROMEDRIVER_VERSION).install()
        else:
            capabilities["chromedriverExecutable"] = ChromeDriverManager().install()
        return BrowserFactory.get_appium_driver(capabilities)

    @staticmethod
    def get_remote_driver(browser_name, browser_version, options=None, browser_profile=None, capabilities=None):
        capabilities["browserName"] = browser_name
        capabilities["version"] = browser_version
        capabilities["enableVNC"] = config.IS_VNC_ENABLED
        capabilities["enableVideo"] = config.IS_VIDEO_ENABLED
        return webdriver.Remote(command_executor=config.SELENOID_URL,
                                desired_capabilities=capabilities, options=options,
                                browser_profile=browser_profile)

    @staticmethod
    def get_appium_driver(capabilities):
        capabilities["nativeWebScreenshot"] = True
        capabilities["androidScreenshotPath"] = "screenshots"
        capabilities["platformName"] = config.BROWSER
        capabilities["platformVersion"] = config.MOBILE_PLATFORM_VERSION
        capabilities["deviceName"] = config.MOBILE_DEVICE_NAME
        if config.MOBILE_UDID:
            capabilities["udid"] = config.MOBILE_UDID
        return appiumdriver.Remote(command_executor=config.APPIUM_URL,
                                   desired_capabilities=capabilities)
