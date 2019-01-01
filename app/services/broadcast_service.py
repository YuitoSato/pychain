import json

import requests

from app.infra.sqlite import PeerNodeDb


class BroadcastService:
    HEADERS = { 'content-type': 'application/json' }

    @classmethod
    def broadcast_transaction(cls, transaction_request, transaction_id):
        nodes = PeerNodeDb.list()

        payload = {
            'transaction_id': transaction_id,
            'request': transaction_request
        }

        for node in nodes:
            requests.post(node.url, data = json.dumps(payload), headers = cls.HEADERS)
