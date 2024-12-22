import re


class StringUtil:

    @staticmethod
    def get_text_without_comma(str_text):
        return str_text.replace(',', '')

    @staticmethod
    def get_text_after_splitting_by_comma(str_text):
        return str_text.split(",")

    @staticmethod
    def get_text_without_dot(str_text):
        return str_text.replace('.', '')

    @staticmethod
    def get_text_without_letters(str_text):
        return re.search('[\d,]+', str_text).group(0)

    @staticmethod
    def get_digits_with_2_and_more_signs(str_text):
        return re.search('(\d{2,})', str_text).group(0)

    @staticmethod
    def get_text_without_percentage(text):
        return text.replace('%', '')

    @staticmethod
    def get_text_only_digits(str_text):
        return re.search('[\d,]+', str_text).group(0).replace(',', '')

    @staticmethod
    def get_title_text(str_text):
        return str_text.upper()

    @staticmethod
    def get_text_from_position(element, position):
        """
        Get any text from specific position in locator after splitting by space
        :return: str: text
        """
        return element.split(" ")[position]

    @staticmethod
    def get_url_from_email(url_regex, body_text):
        return re.search(url_regex, body_text).group(0)

    @staticmethod
    def get_method_name_for_allure_report(test_name):
        return StringUtil.get_text_without_dot(re.search("\.(?:.(?!\.))+$", str(test_name)).group(0))
