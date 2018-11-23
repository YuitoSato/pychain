import json

from flask import jsonify

from app.utils.pychain_encoder import PychainEncoder
from app.models.block import Block
from app.models.proof_of_work import ProofOfWork
from app.models.transaction import Transaction
import hashlib


class MiningController:
    def __init__(self, blockchain, node_address):
        self.blockchain = blockchain
        self.node_address = node_address

    def mine(self):
        transaction = Transaction(
            sender_address="0",
            recipient_address=self.node_address,
            amount=1
        )
        self.blockchain.append_transaction(transaction)
        last_block = self.blockchain.last_block
        last_nonce = last_block.nonce
        proof_of_work = ProofOfWork(last_nonce, 10)
        proof_result = proof_of_work.prove()

        # if not(proof_result.isValid()):

        block_string = json.dumps(last_block, sort_keys=True, cls=PychainEncoder).encode()
        previous_hash = hashlib.sha256(block_string).hexdigest()

        block = Block(
            index=len(self.blockchain.blocks) + 1,
            transactions=self.blockchain.current_transactions,
            nonce=proof_result.nonce,
            previous_hash=hashlib
        )

        self.blockchain.append_block(block)
        self.blockchain.current_transactions = []

        return jsonify(block), 201
