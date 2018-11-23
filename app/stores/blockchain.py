class Blockchain:
    def __init__(self, genesis_block):
        self.blocks = [genesis_block]
        self.current_transactions = []
        self.nodes = []

    def append_transaction(self, transaction):
        self.current_transactions.append(transaction)

    def append_block(self, block):
        self.blocks.append(block)

    @property
    def last_block(self):
        return self.blocks[-1]
