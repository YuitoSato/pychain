from time import time

from flask.json import jsonify

from app.models.transaction import Transaction


class TransactionController:
    def __init__(self, blockchain, hash_converter):
        self.blockchain = blockchain
        self.hash_converter = hash_converter

    def create_transaction(self, request):
        values = request.get_json()
        request_str = (str(time()) + str(values)).encode('utr-8')
        transaction_hash = self.hash_converter.hash(request_str)
        transaction = Transaction(transaction_hash, values['sender'], values['recipient'], values['amount'])

        self.blockchain.append_transaction(transaction)
        index = self.blockchain.last_block.index + 1
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201

    def fetch_current_transactions(self):
        current_transactions = self.blockchain.current_transactions
        return jsonify(current_transactions), 200
