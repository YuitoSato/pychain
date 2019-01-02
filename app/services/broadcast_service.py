import json

import requests

from app.models.peer_node import PeerNode
from app.utils.pychain_encoder import PychainEncoder


class BroadcastService:
    HEADERS = { 'content-type': 'application/json' }

    @classmethod
    def broadcast_transaction(cls, transaction):
        nodes = PeerNode.list()

        for node in nodes:
            requests.post(node.url + '/transactions/receive', data = json.dumps(transaction, cls = PychainEncoder), headers = cls.HEADERS)

    @classmethod
    def broadcast_block(cls, block, proof_result, miner_url):
        nodes = PeerNode.list()

        payload = {
            'block': block,
            'proof_result': proof_result,
            'sender_node_address': miner_url
        }

        for node in nodes:
            requests.post(node.url + '/blocks/receive', data = json.dumps(payload, cls = PychainEncoder), headers = cls.HEADERS)
