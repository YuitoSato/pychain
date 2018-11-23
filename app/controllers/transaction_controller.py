from flask.json import jsonify

from app.models.transaction import Transaction


class TransactionController:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def create_transaction(self, request):
        values = request.get_json()
        transaction = Transaction(values['sender'], values['recipient'], values['amount'])
        self.blockchain.append_transaction(transaction)
        index = self.blockchain.last_block.index + 1
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201

    def fetch_current_transactions(self):
        current_transactions = self.blockchain.current_transactions
        return jsonify(current_transactions), 200
