class Transaction:
    def __init__(
        self,
        transaction_hash,
        sender_address,
        recipient_address,
        amount,
        transaction_outputs,
        transaction_inputs
    ):
        self.transaction_hash = transaction_hash
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount
        self.transaction_outputs = transaction_outputs
        self.transaction_inputs = transaction_inputs
