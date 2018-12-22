from flask import jsonify

from app.utils.pychain_decorder import decode_block


class BlockController:
    def __init__(self, block_service):
        self.block_service = block_service

    def list_blocks(self):
        blocks = self.block_service.list_blocks()
        return jsonify(blocks), 200

    def verify_block(self, request):
        block_from_peer = decode_block(request)
        self.block_service.verify_block(block_from_peer)
