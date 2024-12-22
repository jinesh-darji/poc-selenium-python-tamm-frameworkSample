from framework.configuration import config
from framework.utils.EnvReader import EnvReader
from framework.utils.JSONReader import JSONReader


class LocatorReader(object):

    def __init__(self, page_name):
        self.page_name = page_name
        self.elements_list = JSONReader.read(config.ELEMENTS_PATH)
        self.locale_dict = EnvReader().get_locale_dict()

    def read_locator(self, element_key):
        locator_info = self.elements_list[self.page_name][element_key]
        if locator_info.get("locale_path"):
            locale_text = self.locale_dict
            for key in locator_info.get("locale_path").split("."):
                locale_text = locale_text[key]
            locator_info["locator"] = locator_info["locator"].format(locale_text)
        return locator_info["name"], locator_info["locator"], locator_info["search_cond"]
