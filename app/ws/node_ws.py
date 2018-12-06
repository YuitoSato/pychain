import requests
from flask.json import jsonify


class NodeWs:
    @classmethod
    def send_new_transaction_to_node(node, transaction):
        payload = jsonify(transaction)
        response = requests.post(node, data = payload)
        return response.status_code
