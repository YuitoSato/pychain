import requests
from flask.json import jsonify


class UnconfirmedTransactionWS:
    def __init__(self):
        self.http = requests

    def send_transaction(self, node, transaction):
        payload = jsonify(transaction)
        response = self.http.post(node, data = payload)
        return response.status_code
