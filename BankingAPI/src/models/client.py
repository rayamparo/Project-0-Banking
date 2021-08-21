from src.models.account import Account
from json import JSONEncoder, dumps

class Client:

    def __init__(self, client_id, client_name, client_accounts_list):
        self._client_id = client_id
        self._client_name = client_name
        self._client_accounts = client_accounts_list

class ClientEncoder(JSONEncoder):
    def default(self, class_obj):
        if isinstance(class_obj, Client):
            return class_obj.__dict__
        elif isinstance(class_obj, Account):
            return class_obj.__dict__
        else:
            return super().default(self, class_obj)


