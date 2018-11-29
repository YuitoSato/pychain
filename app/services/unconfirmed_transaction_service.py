class UnconfirmedTransactionService:
    def __init__(self, unconfirmed_transaction_repository, blockchain_repository):
        self.unconfirmed_transaction_repository = unconfirmed_transaction_repository
        self.blockchain_repository = blockchain_repository

    def create_transaction(self, transaction):
        self.unconfirmed_transaction_repository.create_transaction(transaction)
        next_block_num = self.blockchain_repository.find_last_block().index + 1
        return next_block_num

    def list_unconfirmed_transactions(self):
        return self.unconfirmed_transaction_repository.list_all()
