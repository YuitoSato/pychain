class UnconfirmedTransactionRepository:
    def __init__(self):
        self.unconfirmed_transactions = []

    def delete_all(self):
        self.unconfirmed_transactions = []

    def create_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def list_unconfirmed_transactions(self):
        return self.unconfirmed_transactions
