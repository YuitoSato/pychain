from time import time

from app.models.block import Block
from app.models.proof_of_work import ProofOfWork
from app.models.transaction import Transaction


class MiningService:
    def __init__(
        self,
        unconfirmed_transaction_repository,
        blockchain_repository,
        my_node_repository,
        node_repository,
        block_ws,
        node_address,
        hash_converter
    ):
        self.unconfirmed_transaction_repository = unconfirmed_transaction_repository
        self.blockchain_repository = blockchain_repository
        self.my_node_repository = my_node_repository
        self.node_repository = node_repository
        self.block_ws = block_ws
        self.node_address = node_address
        self.hash_converter = hash_converter

    def mine(self):
        transaction_hash = self.hash_converter.hash(str(time()) + self.node_address)

        my_node = self.my_node_repository.find_my_node()
        transaction = Transaction(
            transaction_hash = transaction_hash,
            sender_address = "0",
            recipient_address = my_node.address,
            amount = 1
        )
        self.unconfirmed_transaction_repository.create_transaction(transaction)
        last_block = self.blockchain_repository.find_last_block()
        previous_hash = self.hash_converter.hash(last_block)
        proof_of_work = ProofOfWork(previous_hash, 10)
        proof_result = proof_of_work.prove()

        # if not(proof_result.isValid()):

        blocks = self.blockchain_repository.list_blocks()
        print(blocks)
        unconfirmed_transactions = self.unconfirmed_transaction_repository.list_unconfirmed_transactions()
        self.unconfirmed_transaction_repository.delete_all()

        block = Block(
            index = len(blocks) + 1,
            transactions = unconfirmed_transactions,
            nonce = proof_result.nonce,
            previous_hash = previous_hash,
            difficulty = last_block.difficulty
        )
        self.blockchain_repository.create_block(block)

        nodes = self.node_repository.list_nodes()

        for node in nodes:
            self.block_ws.send_block(
                node = node,
                block = block
            )

        return block
