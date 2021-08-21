from src.models.account import Account
import src.dao.account_dao as account_dao
from re import sub
from decimal import Decimal
import logging
from json import loads

# Logs for data received from services file
logging.basicConfig(filename='account_service.log', level=logging.INFO)

# Transform account data into returnable JSON data for a client
def db_accounts_transform(account_rows):
    account_list = []
    count = 0
    if len(account_rows) > 0:
        for account in account_rows:
            account_list.insert(count, Account(account[0], account[1], account[2], account[3], account[4]))
            count + 1
    return account_list

# Creates new account for client
def create_new_account(client_id, req_body):
    account_dao.create_new_account(client_id, req_body)

# Gets accounts for specific client
def get_specific_accounts(client_id):
    client_accounts_row = account_dao.get_specific_accounts(client_id)
    logging.info(type(db_accounts_transform(client_accounts_row)))
    return db_accounts_transform(client_accounts_row)

# Gets specific accounts within a range for a client
def get_specific_range_accounts(client_id, less_than, greater_than):
    client_accounts = []
    count = 0
    client_accounts_row = account_dao.get_specific_accounts(client_id)
    for account in client_accounts_row:
        float_amount = Decimal(sub(r'[^\d.]', '', account[3]))
        if float_amount < less_than and float_amount > greater_than:
            client_accounts.insert(count, account)
            count + 1
    return db_accounts_transform(client_accounts)

# Gets ONE specific account for client
def get_one_account(client_id, account_id):
    client_row = account_dao.get_one_account(client_id, account_id)
    return db_accounts_transform(client_row)

# Updates account for client
def update_account(client_id, account_id, req_body):
    account_dao.update_account(client_id, account_id, req_body)

# Deletes account for client
def delete_account(client_id, account_id):
    account_dao.delete_account(client_id, account_id)

# Deposit or withdraw from client's account
def deposit_withdraw(client_id, account_id, req_body):
    account_row = account_dao.get_one_account(client_id, account_id)
    float_amount = float(Decimal(sub(r'[^\d.]', '', account_row[0][3])))
    # Logging to make sure the amount is a float type
    logging.info(float_amount)
    if 'withdraw' in req_body:
        withdraw_amount = req_body['withdraw']
        if float_amount >= withdraw_amount:
            amount_after = float_amount - withdraw_amount
            account_dao.deposit_withdraw(client_id, account_id, amount_after)
        else:
            return 'Not enough in account to withdraw'
    if 'deposit' in req_body:
        deposit_amount = req_body['deposit']
        amount_after = float_amount + deposit_amount
        account_dao.deposit_withdraw(client_id, account_id, amount_after)

# Transfer funds between accounts
def transfer_funds(client_id, account_id, account_id_two, req_body):
    account_row = account_dao.get_one_account(client_id, account_id)
    float_amount = float(Decimal(sub(r'[^\d.]', '', account_row[0][3])))
    account_row_two = account_dao.get_one_account(client_id, account_id_two)
    float_amount_two = float(Decimal(sub(r'[^\d.]', '', account_row_two[0][3])))
    amount_transferred = req_body['amount']
    if float_amount >= amount_transferred:
        deducted_amount = float_amount - amount_transferred
        added_amount = float_amount_two + amount_transferred
        account_dao.transfer_funds(client_id, account_id, account_id_two, deducted_amount, added_amount)
    else:
        return 'Not enough in first account to transfer'