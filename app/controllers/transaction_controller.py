from flask.json import jsonify

from app.database.unconfirmed_transaction_pool import UnconfirmedTransactionPool
from app.services.broadcast_service import BroadcastService
from app.services.transaction_service import TransactionService


class TransactionController:
    @classmethod
    def create_transaction(cls, request):
        print('start creating transaction...')
        transaction_request = request.get_json()
        transaction = TransactionService.create_transaction(transaction_request)
        print('created')
        BroadcastService.broadcast_transaction(transaction_request, transaction.transaction_id)
        print('broadcasted')
        return jsonify({}), 201

    @classmethod
    def receive_transaction(cls, request):
        print('receiveed')
        request = request.get_json()
        is_new = TransactionService.assert_new_transaction(request['transaction_id'])
        if not is_new:
            return jsonify({}), 304
        print('start creating transaction...')
        transaction_request = request['transaction_request']
        transaction = TransactionService.create_transaction(transaction_request)
        print(transaction)
        BroadcastService.broadcast_transaction(transaction_request, transaction.transaction_id)
        print('broadcasted')
        return jsonify({}), 201

    @classmethod
    def list_unconfirmed(cls):
        return jsonify(UnconfirmedTransactionPool.transactions), 200
