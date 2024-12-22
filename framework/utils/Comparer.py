from framework.utils.StringUtil import StringUtil


class Comparer:

    @staticmethod
    def check_include_1_list_to_second(a, b):
        return set(a) & (set(b)) == set(a)

    @staticmethod
    def get_and_compare_item_with_each_items_in_list(item_locator, unit_lbl):
        global bool_value
        item_locator.wait_until_location_stable()
        units = item_locator.get_elements_text()
        for i in units:
            if i == unit_lbl:
                bool_value = True
            else:
                bool_value = False
        return bool_value

    @staticmethod
    def get_and_compare_item_in_range(values_list, list_of_data_locator):
        global bool_value
        list_of_data_locator.wait_until_location_stable()
        items = list_of_data_locator.get_elements_text()
        for i in items:
            if int(StringUtil.get_text_only_digits(i)) in range(int(StringUtil.get_text_without_comma(values_list[0])),
                                                                int(StringUtil.get_text_without_comma(
                                                                    values_list[1])) + 1):
                bool_value = True
            else:
                bool_value = False
        return bool_value

    @staticmethod
    def get_and_check_sort_asc(list_of_data):
        list_of_data.wait_until_location_stable()
        items = list_of_data.get_list_of_digits()
        return all(a <= b for a, b in zip(items, items[1:]))

    @staticmethod
    def get_and_check_sort_desc(list_of_data):
        list_of_data.wait_until_location_stable()
        items = list_of_data.get_list_of_digits()
        list_of_digits_test = items
        list_of_digits_test.sort(reverse=True)
        return items == list_of_digits_test
