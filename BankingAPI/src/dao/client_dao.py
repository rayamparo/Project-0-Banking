from src.utils.db import db_connection

# Gets all clients
def get_all_clients():
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute('select * from clients')
        query_rows = cur.fetchall()
    finally:
        con.close()
    return query_rows

# Creates new client
def create_new_client(client):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute("insert into clients values(default, %s)", (client["client_name"],))
        con.commit()
    finally:
        con.close()

# Gets specific client
def get_specific_client(client_id):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'select * from clients where client_id = {client_id}')
        specific_client = cur.fetchall()
    finally:
        con.close()
    return specific_client

# Updates specific client (PUT)
def update_specific_client(client_id, req_body):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'update clients set client_name = %s where client_id = {client_id}', (req_body['client_name'],))
        con.commit()
    finally:
        con.close()

# Deletes a client
def delete_client(client_id):
    try:
        con = db_connection()
        cur = con.cursor()
        cur.execute(f'delete from clients where client_id = {client_id}')
        con.commit()
    finally:
        con.close()

