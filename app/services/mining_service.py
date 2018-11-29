from time import time

from app.models.block import Block
from app.models.proof_of_work import ProofOfWork
from app.models.transaction import Transaction


class MiningService:
    def __init__(self, unconfirmed_transaction_repository, blockchain_repository, node_address, hash_converter):
        self.unconfirmed_transaction_repository = unconfirmed_transaction_repository
        self.blockchain_repository = blockchain_repository
        self.node_address = node_address
        self.hash_converter = hash_converter

    def mine(self):
        transaction_hash = self.hash_converter.hash(str(time()) + self.node_address)
        transaction = Transaction(
            transaction_hash = transaction_hash,
            sender_address = "0",
            recipient_address = self.node_address,
            amount = 1
        )
        self.unconfirmed_transaction_repository.create_transaction(transaction)
        last_block = self.blockchain_repository.find_last_block()
        last_nonce = last_block.nonce
        proof_of_work = ProofOfWork(last_nonce, 10)
        proof_result = proof_of_work.prove()

        # if not(proof_result.isValid()):

        previous_hash = self.hash_converter.hash(last_block)

        blocks = self.blockchain_repository.list_blocks()
        print(blocks)
        unconfirmed_transactions = self.unconfirmed_transaction_repository.list_unconfirmed_transactions()

        block = Block(
            index = len(blocks) + 1,
            transactions = unconfirmed_transactions,
            nonce = proof_result.nonce,
            previous_hash = previous_hash
        )

        self.blockchain_repository.create_block(block)
        self.unconfirmed_transaction_repository.delete_all()

        return block
