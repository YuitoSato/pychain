from flask.json import jsonify

from app.models.transaction import Transaction


class UnconfirmedTransactionController:
    def __init__(self, unconfirmed_transaction_service, hash_converter):
        self.unconfirmed_transaction_service = unconfirmed_transaction_service
        self.hash_converter = hash_converter

    # {
    #   sender_address: string
    #   recipient_address: string,
    #   amount: integer,
    #   transaction_inputs: [
    #     {
    #        transaction_input_id: integer,
    #        unlocking_script: string
    #     }
    #   ]
    # }
    def create_transaction(self, request):
        self.unconfirmed_transaction_service.create_transaction(
            request.get_json()
        )
        return jsonify({ }), 201

    def list_unconfirmed_transactions(self):
        unconfirmed_transactions = self.unconfirmed_transaction_service.list_unconfirmed_transactions()
        return jsonify(unconfirmed_transactions), 200
