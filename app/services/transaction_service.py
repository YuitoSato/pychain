import uuid
from functools import reduce

from app.infra.sqlite.database import db
from app.infra.sqlite.transaction_db import TransactionDb
from app.infra.sqlite.transaction_output_db import TransactionOutputDb
from app.models.transaction import Transaction
from app.models.transaction_output import TransactionOutput
from app.utils.constants import COINBASE_ADDRESS


class TransactionService:
    # {
    #   sender_address: string
    #   recipient_address: string,
    #   amount: integer,
    #   transaction_inputs: [
    #     {
    #        transaction_output_id: integer,
    #        unlocking_script: string
    #     }
    #   ]
    # }
    @classmethod
    def create_transaction(cls, request):
        transaction_inputs_r = request['transaction_inputs']
        sender_address = request['sender_address']
        recipient_address = request['recipient_address']
        request_amount = int(request['amount'])

        session = db.session

        transaction_inputs = list(map(
            lambda transaction_input: TransactionOutputDb.find_unspent(
                transaction_input['transaction_output_id']
            ).to_input(transaction_input['unlocking_script']), transaction_inputs_r
        ))

        transaction_inputs = list(filter(None, transaction_inputs))

        verify_results = list(map(lambda input: input.verify(sender_address), transaction_inputs))
        if False in verify_results:
            raise Exception('error.cant_verify_input')

        transaction_input_amounts = list(map(lambda input: input.amount, transaction_inputs))
        transaction_input_amount_sum = reduce((lambda x, y: x + y), transaction_input_amounts)

        if request_amount > transaction_input_amount_sum:
            raise Exception('error.not_enough_input_amount')

        transaction_id = uuid.uuid1().hex
        to_sender_amount = request_amount * 0.99

        to_sender_transaction_output = TransactionOutput(
            transaction_output_id = uuid.uuid1().hex,
            transaction_id = transaction_id,
            amount = to_sender_amount,
            sender_address = sender_address,
            recipient_address = recipient_address,
        )

        to_coinbase_amount = TransactionOutput(
            transaction_output_id = uuid.uuid1().hex,
            transaction_id = transaction_id,
            amount = request_amount - to_sender_amount,
            sender_address = sender_address,
            recipient_address = COINBASE_ADDRESS
        )

        to_recipient_amount = TransactionOutput(
            transaction_output_id = uuid.uuid1().hex,
            transaction_id = transaction_id,
            amount = transaction_input_amount_sum - request_amount,
            sender_address = sender_address,
            recipient_address = sender_address
        )

        transaction_outputs = [to_sender_transaction_output, to_coinbase_amount, to_recipient_amount]

        transaction = Transaction(
            transaction_id = transaction_id,
            transaction_outputs = transaction_outputs,
            transaction_inputs = transaction_inputs,
            locktime = 0
        )

        TransactionDb.create_transaction(session, transaction)
        session.commit()

        return transaction_id

    @classmethod
    def assert_new_transaction(cls, transaction_id):
        transaction = TransactionDb.find(transaction_id)
        return transaction is not None
