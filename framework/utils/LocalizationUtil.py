import re


class LocalizationUtil:

    @staticmethod
    def get_text_from_page(data_text):
        data_text_lower_case = data_text[0].lower()
        string_text = "".join(re.findall('[A-Za-zء-ي]+', data_text_lower_case))
        return list(set(string_text))

    @staticmethod
    def get_words_from_text(data_text):
        data_text_lower_case = data_text[0].lower()
        list_words = [word for word in re.findall('[A-Za-zء-ي]+', data_text_lower_case) if word != "english"]
        return list_words

    @staticmethod
    def check_localization(data_text):
        page_text = LocalizationUtil.get_text_from_page(data_text)
        return LocalizationUtil.find_en_words_in_ar_text(page_text, data_text)

    @staticmethod
    def find_en_words_in_ar_text(page_text, data_text):
        list_of_not_matching_letters = []
        list_of_words_with_localization_issues = []
        list_of_words = LocalizationUtil.get_words_from_text(data_text)
        for i in page_text:
            if not u'\u0600' <= i <= u'\u06FF':
                list_of_not_matching_letters.append(i)
        for x in list_of_not_matching_letters:
            list_of_words_with_localization_issues = list_of_words_with_localization_issues + \
                                                     [s for s in list_of_words if x in s]
        return list(set(list_of_words_with_localization_issues))
