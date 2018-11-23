from json import JSONEncoder

from app.models.block import Block
from app.models.transaction import Transaction


class PychainEncorder(JSONEncoder):
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
                'sender': o.sender_address,
                'recipient': o.recipient_address,
                'amount': o.amount,
            }
