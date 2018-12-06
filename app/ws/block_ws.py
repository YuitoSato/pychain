import requests
from flask.json import jsonify


class BlockWs:
    def __init__(self):
        self.http = requests

    def send_block(self, node, block):
        payload = jsonify(block)
        response = self.http.post(node + '/blocks', data = payload)
        return response.status_code
