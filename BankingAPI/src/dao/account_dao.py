from src.utils.db import db_connection

# Gets specific accounts for client
def get_specific_accounts(client_id):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'select * from accounts where owner_id = {client_id}')
        client_accounts = cur.fetchall()
        return client_accounts
    finally:
        con.close()

# Creates new account for client
def create_new_account(client_id, req_body):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'insert into accounts values ({client_id}, default, %s, %s, %s)', (req_body['account_category'], req_body['account_amount'], req_body['account_number']))
        con.commit()
    finally:
        con.close()

# Gets ONE specific account for client
def get_one_account(client_id, account_id):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'select * from accounts where (owner_id = {client_id} and account_id = {account_id})')
        account_row = cur.fetchall()
        return account_row
    finally:
        con.close()

# Updates an account
def update_account(client_id, account_id, req_body):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f"""update accounts set account_category = %s, account_amount = %s, account_number = %s
        where (owner_id = {client_id} and account_id = {account_id})""", (req_body['account_category'], req_body['account_amount'], req_body['account_number']))
        con.commit()
    finally:
        con.close()

# Deletes an account for client
def delete_account(client_id, account_id):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'delete from accounts where (owner_id = {client_id} and account_id = {account_id})')
        con.commit()
    finally:
        con.close()

# Deposits and Withdraws from client's account
def deposit_withdraw(client_id, account_id, amount_after):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'update accounts set account_amount = %s where (owner_id = {client_id} and account_id = {account_id})', (amount_after,))
        con.commit()
    finally:
        con.close()

# Transfers funds between client's accounts
def transfer_funds(client_id, account_id, account_id_two, deducted_amount, added_amount):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'update accounts set account_amount = %s where (owner_id = {client_id} and account_id = {account_id})', (deducted_amount,))
        cur.execute(f'update accounts set account_amount = %s where (owner_id = {client_id} and account_id = {account_id_two})', (added_amount,))
        con.commit()
    finally:
        con.close()