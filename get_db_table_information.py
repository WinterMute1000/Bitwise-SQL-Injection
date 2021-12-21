from requests import request
from requests.utils import requote_uri

class GetDbTableInformationClass:
    # Insert target url
    TARGET_URL = ''
    def __init__(self):
        self.SUCCESS_LENGTH = request(url=self.TARGET_URL)
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
    # Getter
    def db_name_getter(self): return self.db_name
    def tables_name_getter(self): return self.tables_name
