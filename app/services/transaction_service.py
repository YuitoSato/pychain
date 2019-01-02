from functools import reduce

from app.database.unconfirmed_transaction_pool import UnconfirmedTransactionPool
from app.model.transaction import Transaction
from app.model.transaction_output import TransactionOutput
from app.utils.constants import COINBASE_ADDRESS


class TransactionService:
    # {
    #   sender_address: string
    #   recipient_address: string,
    #   amount: integer,
    #   timestamp: integer,
    #   transaction_inputs: [
    #     {
    #        transaction_output_id: integer,
    #        unlocking_script: string
    #     }
    #   ]
    # }
    @classmethod
    def create_transaction(cls, request):
        transaction_input_dicts = request['transaction_inputs']
        sender_address = request['sender_address']
        recipient_address = request['recipient_address']
        request_amount = request['amount']
        timestamp = request['timestamp']

        unspent_transaction_outputs = list(filter(lambda tx_output: tx_output['tx_o'] is not None, list(map(
            lambda tx_input: {
                'tx_o': TransactionOutput.find_unspent(tx_input['transaction_output_id']),
                'unlocking_script': tx_input['unlocking_script']
            }, transaction_input_dicts
        ))))

        transaction_inputs = list(map(
            lambda tx_output: tx_output['tx_o'].to_input(tx_output['unlocking_script']), unspent_transaction_outputs
        ))

        verify_results = list(map(lambda input: input.verify(sender_address), transaction_inputs))
        if False in verify_results:
            raise Exception('error.cant_verify_input')

        if len(transaction_inputs) == 0:
            raise Exception('error.not_enough_input_amount')

        transaction_input_amounts = list(map(lambda input: input.transaction_output.amount, transaction_inputs))
        transaction_input_amount_sum = reduce((lambda x, y: x + y), transaction_input_amounts)

        if request_amount > transaction_input_amount_sum:
            raise Exception('error.not_enough_input_amount')

        to_sender_amount = request_amount * 0.99

        transaction = Transaction.build(
            block_id = None,
            locktime = 0,
            timestamp = timestamp
        )

        to_sender_transaction_output = TransactionOutput.build(
            transaction_id = transaction.transaction_id,
            amount = to_sender_amount,
            sender_address = sender_address,
            recipient_address = recipient_address,
            timestamp = timestamp
        )

        to_coinbase_amount = TransactionOutput.build(
            transaction_id = transaction.transaction_id,
            amount = request_amount - to_sender_amount,
            sender_address = sender_address,
            recipient_address = COINBASE_ADDRESS,
            timestamp = timestamp
        )

        to_recipient_amount = TransactionOutput.build(
            transaction_id = transaction.transaction_id,
            amount = transaction_input_amount_sum - request_amount,
            sender_address = sender_address,
            recipient_address = sender_address,
            timestamp = timestamp
        )

        transaction_outputs = [to_sender_transaction_output, to_coinbase_amount, to_recipient_amount]
        transaction.transaction_outputs = transaction_outputs
        transaction.transaction_inputs = transaction_inputs

        UnconfirmedTransactionPool.transactions.append(transaction)

        return transaction

    @classmethod
    def assert_new_transaction(cls, transaction_id):
        transactions = list(filter(lambda tx: tx.transaction_id == transaction_id, UnconfirmedTransactionPool.transactions))
        return len(transactions) == 0
