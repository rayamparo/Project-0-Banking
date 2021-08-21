from src.app import app
from src.models.client import ClientEncoder
from flask import request, Response
from json import dumps
import logging
from src.service.client_service import get_specific_client
import src.service.account_service as account_service

# Logs for account controller
logging.basicConfig(filename='account_controller.log', level=logging.INFO)

@app.route('/clients/<int:client_id>/accounts', methods=['POST', 'GET'])
def clients_accounts(client_id):
    # POST
    if request.method == 'POST':
        if get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        req_body = request.get_json()
        account_service.create_new_account(client_id, req_body)
        return Response('Account successfully created for client', status=201)
    # GET with no query parameters
    if request.method == 'GET' and request.args.get('amountLessThan') is None and request.args.get('amountGreaterThan') is None:
        if get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        return dumps(account_service.get_specific_accounts(client_id), cls=ClientEncoder)
    # GET WITH query parameters
    if request.method == 'GET':
        if get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        less_than = float(request.args.get('amountLessThan'))
        greater_than = float(request.args.get('amountGreaterThan'))
        return dumps(account_service.get_specific_range_accounts(client_id, less_than, greater_than), cls=ClientEncoder)

@app.route('/clients/<int:client_id>/accounts/<int:account_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def clients_specific_accounts(client_id, account_id):
    # GET
    if request.method == 'GET':
        if get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        logging.info(account_service.get_one_account(client_id, account_id))
        if account_service.get_one_account(client_id, account_id) == []:
            return Response('Client does not have an account corresponding to account number given', status=404)
        return dumps(account_service.get_one_account(client_id, account_id), cls=ClientEncoder)
    # PUT
    if request.method == 'PUT':
        if get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        if account_service.get_one_account(client_id, account_id) == []:
            return Response('Client does not have an account corresponding to account number given', status=404)
        req_body = request.get_json()
        account_service.update_account(client_id, account_id, req_body)
        return Response('Account successfully updated', status=200)
    # DELETE
    if request.method == 'DELETE':
        if get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        if account_service.get_one_account(client_id, account_id) == []:
            return Response('Client does not have an account corresponding to account number given', status=404)
        account_service.delete_account(client_id, account_id)
        return Response('Account successfully deleted', status=205)
    # PATCH
    if request.method == 'PATCH':
        if get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        if account_service.get_one_account(client_id, account_id) == []:
            return Response('Client does not have an account corresponding to account number given', status=404)
        req_body = request.get_json()
        transaction = account_service.deposit_withdraw(client_id, account_id, req_body)
        if transaction == 'Not enough in account to withdraw':
            return Response('Insufficient Funds', status=422)
        return dumps(account_service.get_one_account(client_id, account_id), cls=ClientEncoder)

@app.route('/clients/<int:client_id>/accounts/<int:account_id>/transfer/<int:account_id_two>', methods=['PATCH'])
def transfer_amount_between_accounts(client_id, account_id, account_id_two):
    if get_specific_client(client_id) == {}:
        return Response('No such client exist', status=404)
    if account_service.get_one_account(client_id, account_id) == [] or account_service.get_one_account(client_id, account_id_two) == []:
        return Response('Client does not have an account corresponding to account number given', status=404)
    req_body = request.get_json()
    transfer = account_service.transfer_funds(client_id, account_id, account_id_two, req_body)
    if transfer == 'Not enough in first account to transfer':
        return Response('Insufficient Funds', status=422)
    return Response('Funds successfully transferred', status=200)




