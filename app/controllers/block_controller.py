from flask import jsonify

from app.services.block_service import BlockService
from app.services.broadcast_service import BroadcastService
from app.utils.pychain_decorder import decode_block, decode_proof_result


class BlockController:
    @classmethod
    def list_blocks(cls):
        return jsonify(BlockService.list_blocks()), 200

    @classmethod
    def create_block(cls, host):
        block, proof_result, transaction = BlockService.create_block()
        BroadcastService.broadcast_block(block, proof_result, host)
        BroadcastService.broadcast_transaction(transaction)
        return jsonify({}), 201

    @classmethod
    def receive_block(cls, request):
        print('received block')
        block = decode_block(request.get_json()['block'])
        is_new = BlockService.assert_new_block(block.block_id)
        if not is_new:
            return jsonify({}), 304
        print('start creating block...')
        proof_result = decode_proof_result(request.get_json()['proof_result'])
        BlockService.receive_block(block, proof_result, request.get_json()['sender_node_address'])
        BroadcastService.broadcast_block(block, proof_result, request.host)
        print('broadcasted')

        return jsonify({}), 200

    @classmethod
    def find_by_block_number(cls, block_number):
        return jsonify(BlockService.find_by_block_number(block_number)), 200
