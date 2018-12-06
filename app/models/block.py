from time import time


class Block:
    def __init__(self, index, transactions, nonce, previous_hash, difficulty, timestamp = time()):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.difficulty = difficulty
        self.previous_hash = previous_hash

    @classmethod
    def genesis_block(cls):
        return Block(
            index = 1,
            transactions = [],
            nonce = 100,
            previous_hash = 1,
            difficulty = 10
        )
