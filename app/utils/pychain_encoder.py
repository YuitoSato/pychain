from json import JSONEncoder

from app.models.block import Block
from app.models.node import Node
from app.models.transaction import Transaction


class PychainEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Block):
            return {
                'index': o.index,
                'timestamp': o.timestamp,
                'transactions': o.transactions,
                'nonce': o.nonce,
                'previous_hash': o.previous_hash,
            }
        if isinstance(o, Transaction):
            return {
                'transaction_hash': o.transaction_hash,
                'sender_address': o.sender_address,
                'recipient_address': o.recipient_address,
                'amount': o.amount,
            }
        if isinstance(o, Node):
            return {
                'url': o.url,
                'address': o.address
            }
