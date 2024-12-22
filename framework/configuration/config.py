# Test environment
import os

# Enviroment for running tests
ENV = "qa"

# Browser Settings
# Supported browsers: "chrome", "firefox", "ie", "safari", "remote"
BROWSER = "iOS"

# Headless Settings
# Supported values: "y", "n"
HEADLESS = "n"

# Localization
# Supported locale: "en", "ar"
LOCALE = "en"

# Selenoid Settings (remote browser)
SELENOID_HOST = "0.0.0.0"
SELENOID_PORT = "4444"
SELENOID_URL = "http://{host}:{port}/wd/hub".format(host=SELENOID_HOST, port=SELENOID_PORT)
IS_VNC_ENABLED = True
IS_VIDEO_ENABLED = False
USE_SELENOID = False

# Accessibility
CHECK_ACCESSIBILITY = True

# Mobile
# Android, iOS
MOBILE_PLATFORM_VERSION = "12.1"
# Android Emulator, iPhone X
MOBILE_DEVICE_NAME = "iPhone X"
MOBILE_UDID = None
MOBILE_CHROMEDRIVER_VERSION = "2.40"

APPIUM_HOST = "localhost"
APPIUM_PORT = "4723"
APPIUM_URL = "http://{host}:{port}/wd/hub".format(host=APPIUM_HOST, port=APPIUM_PORT)

# Waiting settings
IS_PRESENT_IMPLICITLY_WAIT_SEC = 30
IMPLICITLY_WAIT_SEC = 30
EXPLICITLY_WAIT_SEC = 30
PAGE_LOAD_TIMEOUT_SEC = 150
SCRIPT_TIMEOUT_SEC = 30
CUSTOM_WAIT_STEPTIME = 1
CYCLE_WAIT_TIMEOUT = 180

ELEMENTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pages', 'elements.json')
PATTERN_ENV_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "environments", "{0}", "")
PATTERN_LOCALE_DICTIONARY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale", "{0}",
                                              "dictionary.json")
PATTERN_LOCALE_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data", "{0}", "data.json")
