import base64
import os
import time

from framework.browser.Browser import Browser
from framework.configuration import config


class UploadFileAndroidForm:
    btn_allow_xpath = "//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']"
    btn_open_files_storage_xpath = "//android.widget.TextView[@text = 'Files']"
    btn_click_file_xpath = "//android.widget.TextView[@text = '{}']"
    MOBILE_CONTEXT = "NATIVE_APP"
    CHROME_CONTEXT = "CHROMIUM"

    def upload_file_android(self, file_name):
        Browser.get_driver().switch_to.context(self.MOBILE_CONTEXT)
        time.sleep(2)
        self.btn_allow = Browser.get_driver().find_elements_by_xpath(self.btn_allow_xpath)
        if len(self.btn_allow) > 0:
            self.btn_allow[0].click()
            self.btn_allow[0].click()
        self.btn_open_files_storage = Browser.get_driver().find_element_by_xpath(self.btn_open_files_storage_xpath)
        self.btn_open_files_storage.click()
        self.btn_click_file_xpath = self.btn_click_file_xpath.format(file_name)
        self.btn_click_file = Browser.get_driver().find_elements_by_xpath(self.btn_click_file_xpath)
        if len(self.btn_click_file) == 0:
            self.push_file(file_name)
            self.btn_click_file = Browser.get_driver().find_elements_by_xpath(self.btn_click_file_xpath)
        self.btn_click_file[0].click()
        Browser.get_driver().switch_to.context(self.CHROME_CONTEXT)

    def push_file(self, file):
        with open(os.path.join(config.TEST_FILES_PATH, file), "rb") as imageFile:
            str = base64.b64encode(imageFile.read())
        Browser.get_driver().push_file("/sdcard/Download/" + file,
                                       str.decode('utf8'))
