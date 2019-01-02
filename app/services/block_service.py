from datetime import datetime
from decimal import Decimal
from functools import reduce

import requests

from app.database.sqlite import db
from app.database.unconfirmed_transaction_pool import UnconfirmedTransactionPool
from app.models.block import Block
from app.models.transaction import Transaction
from app.models.transaction_output import TransactionOutput
from app.models.proof_of_work import ProofOfWork
from app.utils.constants import COINBASE_ADDRESS
from app.utils.pychain_decorder import decode_blocks


class BlockService:
    MINER_ADDRESS = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAznjoHvzCJtQcIYd3yj7v\ngwaPlyiG6U/Qlw1G89n0bNt5anvRe+e2eKzvpy98aj6ShGu7hARE9SxAFA9bIHCB\nqdAyPnrUaw7qGkeZNPHBByHe9prJSn0ZwBtfySOSbzdetO5aAwvLj5qMudW2PDz1\n5mP2taGOvXqNnbcH78ZHQLvF6G+SbwuLHU5LEDSZlcy+CnvPqD67cg+QmJLneVmQ\nfOBtbFHz3yDQghNrHWa+UCspUMHVGsDG6OEK7MSpPieY6TzBEYQWsikosQ+V0zBN\nrSCADe3GBcJ7XzafM/gb+gzJ1eP78F1sA6Ja4ZtqInqN406PwerAXaUJa2twW652\n9wIDAQAB\n-----END PUBLIC KEY-----'

    @classmethod
    def list_blocks(cls):
        return Block.list()

    @classmethod
    def find_by_block_number(cls, block_number):
        return Block.find_by_block_number(block_number)

    @classmethod
    def create_block(cls):
        last_block = Block.last()
        previous_hash = last_block.block_id
        proof_of_work = ProofOfWork(previous_hash, 10)
        proof_result = proof_of_work.prove()

        if not proof_result.isValid():
            raise Exception('fail proof')

        transactions = UnconfirmedTransactionPool.transactions.copy()
        UnconfirmedTransactionPool.transactions.clear()
        block_number = len(Block.list()) + 1

        block = Block.build(
            block_number = block_number,
            version = "1",
            previous_block_hash = previous_hash,
            timestamp = datetime.now().timestamp(),
            merkle_root = "",  # TODO
            difficulty_target = 10,
            nonce = proof_result.nonce,
            transactions = transactions
        )

        for tx in transactions:
            tx.block_id = block.block_id

        Block.create_block(block)

        db.session.commit()

        transaction = cls._create_transaction_to_miner()

        return block, proof_result, transaction

    @classmethod
    def _create_transaction_to_miner(cls):
        transaction_inputs = list(map(
            lambda tx_o: tx_o.to_input(''), TransactionOutput.list_unspent(COINBASE_ADDRESS)
        ))

        transaction_input_amounts = list(map(lambda tx_i: tx_i.transaction_output.amount, transaction_inputs))
        if len(transaction_inputs) == 0:
            transaction_input_amount_sum = Decimal(0)
        else:
            transaction_input_amount_sum = Decimal(reduce((lambda x, y: x + y), transaction_input_amounts))

        transaction = Transaction.build(
            block_id = None,
            locktime = 0,
            timestamp = datetime.now().timestamp()
        )

        transaction_output_to_miner = TransactionOutput.build(
            transaction_id = transaction.transaction_id,
            amount = transaction_input_amount_sum * Decimal(0.99),
            sender_address = COINBASE_ADDRESS,
            recipient_address = cls.MINER_ADDRESS,
            timestamp = datetime.now().timestamp()
        )

        transaction_output_to_coinbase = TransactionOutput.build(
            transaction_id = transaction.transaction_id,
            amount = transaction_input_amount_sum * Decimal(0.99),
            sender_address = COINBASE_ADDRESS,
            recipient_address = COINBASE_ADDRESS,
            timestamp = datetime.now().timestamp()
        )

        transaction.transaction_inputs = transaction_inputs
        transaction.transaction_outputs = [transaction_output_to_miner, transaction_output_to_coinbase]

        UnconfirmedTransactionPool.transactions.append(transaction)

        return transaction

    @classmethod
    def receive_block(cls, block, proof_result, send_node_url):
        last_block = Block.last()

        if not proof_result.isValid():
            raise Exception('received block is invalid')

        if last_block.block_id != block.previous_block_hash:
            if last_block.block_number < block.block_number:
                print('resolving conflicting...')
                cls._resolve_conflicts(send_node_url)

        if last_block.block_id == block.previous_block_hash:
            Block.create_block(block)

        UnconfirmedTransactionPool.transactions.clear()
        db.session.commit()

    @classmethod
    def assert_new_block(cls, block_id):
        block = Block.find(block_id)
        return block is None

    @classmethod
    def _resolve_conflicts(cls, send_node_url):
        json = requests.get(send_node_url + '/blocks').json()
        send_node_blocks = decode_blocks(json)
        my_node_blocks = Block.list()

        forked_block_number = cls._search_forked_block_number(send_node_blocks, my_node_blocks)
        deleting_blocks = list(filter(lambda block: block.block_number > forked_block_number, my_node_blocks))
        adding_blocks = list(filter(lambda block: block.block_number > forked_block_number, send_node_blocks))
        Block.delete_blocks(deleting_blocks)
        Block.create_blocks(adding_blocks)

    @classmethod
    def _search_forked_block_number(cls, blocks1, blocks2):
        for block1 in blocks1:
            for block2 in blocks2:
                if block1.block_id == block2.block_id:
                    return block1.block_number
        return 0
