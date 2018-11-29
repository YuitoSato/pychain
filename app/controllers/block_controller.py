from flask import jsonify


class BlockController:
    def __init__(self, block_service):
        self.block_service = block_service

    def list_blocks(self):
        blocks = self.block_service.list_blocks()
        return jsonify(blocks), 200
