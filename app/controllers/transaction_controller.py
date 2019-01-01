from flask.json import jsonify

from app.services.broadcast_service import BroadcastService
from app.services.transaction_service import TransactionService


class TransactionController:
    @classmethod
    def create_transaction(cls, request):
        transaction_request = request.get_json()
        transaction_id = TransactionService.create_transaction(transaction_request)
        BroadcastService.broadcast_transaction(transaction_request, transaction_id)
        return jsonify({}), 201

    @classmethod
    def receive_transaction(cls, request):
        request = request.get_json()
        is_new = TransactionService.assert_new_transaction(request['transaction_id'])
        if not is_new:
            return jsonify({}), 304

        transaction_request = request['transaction_request']
        transaction_id = TransactionService.create_transaction(transaction_request)
        BroadcastService.broadcast_transaction(transaction_request, transaction_id)
        return jsonify({}), 201
