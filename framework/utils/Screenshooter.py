import logging
import os
import threading
from datetime import datetime

from PIL import Image

from framework.browser.Browser import Browser
from framework.constants import Screenshots
from framework.utils.DatetimeUtil import DatetimeUtil


class Screenshooter:
    __session_dir = None
    __screen_number = Screenshots.NUMBER_OF_FIRST_SCREEN
    __screen_dir = os.path.join(os.getcwd(), Screenshots.PATH_TO_SCREENSHOTS)

    @staticmethod
    def set_session_screen_dir():
        lock = threading.Lock()
        lock.acquire()
        try:
            if not os.path.exists(Screenshooter.__screen_dir):
                logging.info("Creating folder for screenshots: " + Screenshooter.__screen_dir)
                os.makedirs(Screenshooter.__screen_dir)

            new_screen_path = os.path.join(
                Screenshooter.__screen_dir,
                "Session_" + DatetimeUtil.get_str_datetime(Screenshots.FORMAT_DATETIME_FOR_SCREEN))

            if Screenshooter.__session_dir is None and not os.path.exists(new_screen_path):
                Screenshooter.__session_dir = new_screen_path
            else:
                Screenshooter.__session_dir = new_screen_path + "." + str(datetime.now().microsecond)

                logging.info("Folder creating " + new_screen_path)
            os.makedirs(Screenshooter.__session_dir)
        finally:
            lock.release()

    @staticmethod
    def get_screen_file_name(file_format=Screenshots.FILE_FORMAT_PNG):
        scr_number = str(Screenshooter.__screen_number)
        Screenshooter.__screen_number += 1
        return "Screenshot_" + scr_number + file_format

    @staticmethod
    def take_screenshot():
        screen_name = Screenshooter.get_screen_file_name()
        save_screen_path = os.path.join(Screenshooter.__session_dir, screen_name)

        logging.info("Making screenshot to file " + screen_name)
        Browser.get_driver().save_screenshot(save_screen_path)
        im = Image.open(save_screen_path)
        rgb_im = im.convert('RGB')
        save_screen_path = save_screen_path.replace(Screenshots.FILE_FORMAT_PNG, Screenshots.FILE_FORMAT_JPG)
        rgb_im.save(save_screen_path)
        return save_screen_path
