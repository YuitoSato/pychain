from flask import jsonify


class BlockController:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def fetch_blocks(self):
        return jsonify(self.blockchain.blocks), 200
