from time import time

from flask.json import jsonify

from app.models.transaction import Transaction


class UnconfirmedTransactionController:
    def __init__(self, unconfirmed_transaction_service, hash_converter):
        self.unconfirmed_transaction_service = unconfirmed_transaction_service
        self.hash_converter = hash_converter

    def create_transaction(self, request):
        values = request.get_json()
        request_str = (str(time()) + str(values)).encode('utf-8')
        transaction_hash = self.hash_converter.hash(request_str)
        transaction = Transaction(transaction_hash, values['sender'], values['recipient'], values['amount'])
        index = self.unconfirmed_transaction_service.create_transaction(transaction)
        response = { 'message': f'Transaction will be added to Block {index}' }
        return jsonify(response), 201

    def list_unconfirmed_transactions(self):
        unconfirmed_transactions = self.unconfirmed_transaction_service.list_unconfirmed_transactions()
        return jsonify(unconfirmed_transactions ), 200
