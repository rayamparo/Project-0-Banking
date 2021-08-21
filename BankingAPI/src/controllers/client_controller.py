from src.app import app
from src.models.client import ClientEncoder
from flask import request, Response
from json import dumps
import src.service.client_service as client_service
import logging

# Logs for data received from services file
logging.basicConfig(filename='client_controller.log', level=logging.INFO)

@app.route('/clients', methods=['POST', 'GET'])
def get_clients():
    # POST
    if request.method == 'POST':
        req_body = request.get_json()
        client_service.create_new_client(req_body)
        return Response('User created!', status=201)
    # GET
    if request.method == 'GET':
        client_json = dumps(client_service.get_all_clients(), cls=ClientEncoder)
        return client_json

@app.route('/clients/<int:client_id>', methods=['GET', 'PUT', 'DELETE'])
def specific_client(client_id):
    # GET
    if request.method == 'GET':
        logging.info(client_service.get_specific_client(client_id))
        if client_service.get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        specific_client_json = dumps(client_service.get_specific_client(client_id), cls=ClientEncoder)
        return specific_client_json
    # PUT
    if request.method == 'PUT':
        req_body = request.get_json()
        if client_service.get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        else:
            client_service.update_specific_client(client_id, req_body)
            return Response('Client updated', status=201)
    # DELETE
    if request.method == 'DELETE':
        if client_service.get_specific_client(client_id) == {}:
            return Response('No such client exist', status=404)
        else:
            client_service.delete_client(client_id)
            return Response('Client successfully deleted', status=205)