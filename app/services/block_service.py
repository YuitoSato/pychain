import json
from datetime import datetime

import requests

from app.database.sqlite import db
from app.database.unconfirmed_transaction_pool import UnconfirmedTransactionPool
from app.model.block import Block
from app.models.proof_of_work import ProofOfWork
from app.utils.pychain_decorder import decode_blocks
from app.utils.pychain_encoder import PychainEncoder


class BlockService:
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

        print(json.dumps(block, cls = PychainEncoder))

        return block, proof_result

    @classmethod
    def receive_block(cls, block, proof_result, send_node_url):
        last_block = Block.last()

        if not proof_result.isValid():
            raise Exception('received block is invalid')

        if last_block.block_id is not block.previous_block_hash:
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
        send_node_blocks = decode_blocks(requests.get('http://' + send_node_url + '/blocks').json())

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

