import requests
from flask.json import jsonify


class NodeWs:
    def __init__(self):
        self.http = requests

    def send_node(self, target_node, sending_node):
        payload = jsonify(sending_node)
        response = self.http.post(target_node + '/nodes', data = payload)
        return response.status_code
