from flask import jsonify


class MiningController:
    def __init__(self, mining_service):
        self.mining_service = mining_service

    def mine(self):
        block = self.mining_service.mine()
        return jsonify(block), 201
