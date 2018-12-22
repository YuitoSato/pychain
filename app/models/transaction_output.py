class TransactionOutput:
    def __init__(self, transaction_output_id, transaction_id, amount, locking_script, sender_address, recipient_address):
        self.transaction_output_id = transaction_output_id
        self.transaction_id = transaction_id
        self.amount = amount
        self.locking_script = locking_script
        self.sender_address = sender_address
        self.recipient_address = recipient_address
