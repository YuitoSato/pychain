# import json
# import uuid
# from functools import reduce
#
# from app.infra.sqlite.db_conf import DbConf
# from app.infra.sqlite.transaction_db import TransactionDb
# from app.infra.sqlite.transaction_output_db import TransactionOutputDb
# from app.models.transaction import Transaction
# from app.models.transaction_output import TransactionOutput
#
#
# class UnconfirmedTransactionService:
#     def __init__(self, unconfirmed_transaction_repository, blockchain_repository):
#         self.unconfirmed_transaction_repository = unconfirmed_transaction_repository
#         self.blockchain_repository = blockchain_repository
#
#     # {
#     #   sender_address: string
#     #   recipient_address: string,
#     #   amount: integer,
#     #   transaction_inputs: [
#     #     {
#     #        transaction_output_id: integer,
#     #        unlocking_script: string
#     #     }
#     #   ]
#     # }
#     @classmethod
#     def create_transaction(cls, request):
#         transaction_inputs_r = request['transaction_inputs']
#         sender_address = request['sender_address']
#         recipient_address = request['recipient_address']
#         request_amount = int(request['amount'])
#
#         session = DbConf.session
#
#         transaction_inputs = list(map(
#             lambda transaction_input: TransactionOutputDb.find(
#                 session, transaction_input['transaction_output_id']
#             ).to_input(transaction_input['unlocking_script']), transaction_inputs_r
#         ))
#
#         print(transaction_inputs)
#
#         verify_results = list(map(lambda input: input.verify(sender_address), transaction_inputs))
#         if False in verify_results:
#             raise Exception('error.cant_verify_input')
#
#         transaction_input_amounts = list(map(lambda input: input.amount, transaction_inputs))
#         transaction_input_amount_sum = reduce((lambda x, y: x + y), transaction_input_amounts)
#
#         if request_amount > transaction_input_amount_sum:
#             raise Exception('error.not_enough_input_amount')
#
#         transaction_id = uuid.uuid1().int
#         to_sender_amount = request_amount * 0.99
#
#         to_sender_transaction_output = TransactionOutput(
#             transaction_output_id = uuid.uuid1().int,
#             transaction_id = transaction_id,
#             amount = to_sender_amount,
#             locking_script = '1',  # TODO
#             sender_address = sender_address,
#             recipient_address = recipient_address,
#         )
#
#         to_coinbase_amount = TransactionOutput(
#             transaction_output_id = uuid.uuid1().int,
#             transaction_id = transaction_id,
#             amount = request_amount - to_sender_amount,
#             locking_script = '1',
#             sender_address = sender_address,
#             recipient_address = 1
#         )
#
#         to_recipient_amount = TransactionOutput(
#             transaction_output_id = uuid.uuid1().int,
#             transaction_id = transaction_id,
#             amount = transaction_input_amount_sum - request_amount,
#             locking_script = '1',
#             sender_address = sender_address,
#             recipient_address = sender_address
#         )
#
#         transaction_outputs = [to_sender_transaction_output, to_coinbase_amount, to_recipient_amount]
#
#         transaction = Transaction(
#             transaction_id = transaction_id,
#             transaction_outputs = transaction_outputs,
#             transaction_inputs = transaction_inputs,
#             locktime = 0
#         )
#
#         TransactionDb.create_transaction(session, transaction)
#         session.commit()
#
#     def list_unconfirmed_transactions(self):
#         return self.unconfirmed_transaction_repository.list_all()
