from framework.utils.EnvReader import EnvReader


class DataReader(object):
    __data_dict = EnvReader().get_data_dict()

    @staticmethod
    def get_data(data_key):
        data = DataReader.__data_dict
        for key in data_key.split("."):
            data = data[key]
        return data
