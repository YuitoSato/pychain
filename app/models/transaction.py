class Transaction:
    def __init__(self, transaction_hash, sender_address, recipient_address, amount):
        self.transaction_hash = transaction_hash
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount
