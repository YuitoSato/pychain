from decimal import Decimal
from json import JSONEncoder

from app.models.block import Block
from app.models.peer_node import PeerNode
from app.models.transaction import Transaction
from app.models.transaction_input import TransactionInput
from app.models.transaction_output import TransactionOutput
from app.models.proof_result import ProofResult


class PychainEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Block):
            return {
                'block_id': o.block_id,
                'block_number': o.block_number,
                'version': o.version,
                'previous_block_hash': o.previous_block_hash,
                'timestamp': o.timestamp,
                'merkle_root': o.merkle_root,
                'difficulty_target': o.difficulty_target,
                'nonce': o.nonce,
                'transactions': o.transactions
            }
        if isinstance(o, Transaction):
            return {
                'transaction_id': o.transaction_id,
                'block_id': o.block_id,
                'locktime': o.locktime,
                'transaction_inputs': o.transaction_inputs,
                'transaction_outputs': o.transaction_outputs
            }
        if isinstance(o, TransactionOutput):
            return {
                'transaction_output_id': o.transaction_output_id,
                'transaction_id': o.transaction_id,
                'amount': o.amount,
                'locking_script': o.locking_script,
                'sender_address': o.sender_address,
                'recipient_address': o.recipient_address
            }
        if isinstance(o, TransactionInput):
            return {
                'transaction_input_id': o.transaction_input_id,
                'transaction_id': o.transaction_id,
                'transaction_output_id': o.transaction_output_id,
                'unlocking_script': o.unlocking_script,
            }
        if isinstance(o, ProofResult):
            return {
                'result_hash_int': o.result_hash_int,
                'target_hash_int': o.target_hash_int,
                'nonce': o.nonce
            }
        if isinstance(o, PeerNode):
            return {
                'peer_node_id': o.peer_node_id,
                'url': o.url,
                'address': o.address
            }
        if isinstance(o, Decimal):
            return float(o)
        return JSONEncoder.default(self, o)
