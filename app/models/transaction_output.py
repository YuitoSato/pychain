import uuid

from app.models.transaction_input import TransactionInput


class TransactionOutput:
    def __init__(self, transaction_output_id, transaction_id, amount, locking_script, sender_address, recipient_address):
        self.transaction_output_id = transaction_output_id
        self.transaction_id = transaction_id
        self.amount = amount
        self.locking_script = locking_script
        self.sender_address = sender_address
        self.recipient_address = recipient_address

    def to_input(self, unlocking_script):
        TransactionInput(
            transaction_input_id = uuid.uuid1().int,
            transaction_id = self.transaction_id,
            transaction_output_id = self.transaction_output_id,
            amount = self.amount,
            unlocking_script = unlocking_script
        )
