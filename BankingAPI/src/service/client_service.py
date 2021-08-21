import src.dao.client_dao as client_dao
from src.models.client import Client
from src.service.account_service import db_accounts_transform
from src.dao.account_dao import get_specific_accounts
import logging

# Logs
logging.basicConfig(filename='client_service.log', level=logging.INFO)

# Gets all clients
def get_all_clients():
    client_dict = {}
    db_clients = client_dao.get_all_clients()
    for client in db_clients:
        account_rows = get_specific_accounts(client[0])
        account_list = db_accounts_transform(account_rows)
        client_dict[client[0]] = Client(client[0], client[1], account_list)
    return client_dict

# Creates new clients
def create_new_client(client):
    client_dao.create_new_client(client)

# Gets specific client
def get_specific_client(client_id):
     specific_client_dict = {}
     try:
        specific_client = client_dao.get_specific_client(client_id)
        client_account_rows = get_specific_accounts(specific_client[0][0])
        accounts_list = db_accounts_transform(client_account_rows)
        specific_client_dict['1'] = Client(specific_client[0][0], specific_client[0][1], accounts_list)
        return specific_client_dict
     except IndexError:
        # Logs the specific IndexError I was getting when the client row was out of index
        logging.info(IndexError)
        return {}

# Updates specific client (PUT)
def update_specific_client(client_id, req_body):
    client_dao.update_specific_client(client_id, req_body)

# Deletes specific client
def delete_client(client_id):
    client_dao.delete_client(client_id)