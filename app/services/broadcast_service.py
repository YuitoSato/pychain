import json

import requests

from app.infra.sqlite import PeerNode
from app.utils.pychain_encoder import PychainEncoder
from entrypoint import app


class BroadcastService:
    HEADERS = { 'content-type': 'application/json' }

    @classmethod
    def broadcast_transaction(cls, transaction):
        nodes = PeerNode.list()

        for node in nodes:
            requests.post(node.url + '/transactions/receive', data = json.dumps(transaction, cls = PychainEncoder), headers = cls.HEADERS)

    @classmethod
    def broadcast_block(cls, block, proof_result):
        nodes = PeerNode.list()

        payload = {
            'block': block,
            'proof_result': proof_result,
            'sender_node_adderss': 'http://pychain-node' + app.config['NODE_NUMBER'] + '500' + app.config['NODE_NUMBER']
        }

        for node in nodes:
            requests.post(node.url + '/blocks/receive', data = json.dumps(payload, cls = PychainEncoder), headers = cls.HEADERS)
