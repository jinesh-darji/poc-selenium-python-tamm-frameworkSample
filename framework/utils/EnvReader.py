import os

from framework.configuration import config
from framework.utils.JSONReader import JSONReader


class EnvReader:

    def get_data(self, path_to_json):
        return JSONReader.read(path_to_json.format(config.ENV))

    def get_env_variable(self, name, default=None):
        env_value = os.environ.get(name)
        return env_value if env_value else default

    def get_env(self):
        return self.get_env_variable('ENV', config.ENV)

    def get_locale(self):
        return self.get_env_variable('LOCALE', config.LOCALE)

    def get_browser(self):
        return self.get_env_variable('BROWSER', config.BROWSER)

    def get_env_base_path(self):
        return config.PATTERN_ENV_BASE_PATH.format(self.get_env())

    def get_locale_dict(self):
        dict_path = config.PATTERN_LOCALE_DICTIONARY_PATH.format(self.get_locale())
        return self.get_data(dict_path)

    def get_data_dict(self):
        dict_path = config.PATTERN_LOCALE_DATA_PATH.format(self.get_locale())
        return self.get_data(dict_path)

    def get_env_config(self):
        config_path = self.get_env_base_path() + "config.json"
        return self.get_data(config_path)

    def get_from_locale(self, path):
        result = self.get_locale_dict()
        for key in path.split("."):
            result = result[key]
        return result
