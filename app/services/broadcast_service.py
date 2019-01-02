import json

import requests

from app.infra.sqlite import PeerNode
from app.utils.pychain_encoder import PychainEncoder


class BroadcastService:
    HEADERS = { 'content-type': 'application/json' }

    @classmethod
    def broadcast_transaction(cls, transaction_request, transaction_id):
        nodes = PeerNode.list()

        payload = {
            'transaction_id': transaction_id,
            'transaction_request': transaction_request
        }

        for node in nodes:
            requests.post(node.url + '/transactions/receive', data = json.dumps(payload), headers = cls.HEADERS)

    @classmethod
    def broadcast_block(cls, block, proof_result):
        nodes = PeerNode.list()

        payload = {
            'block': block,
            'proof_result': proof_result
        }

        for node in nodes:
            requests.post(node.url + '/blocks/receive', data = json.dumps(payload, cls = PychainEncoder), headers = cls.HEADERS)
