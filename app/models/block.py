from time import time


class Block:
    def __init__(self, block_id, transaction_ids, version, previous_hash, merkle_root, difficulty_target, nonce, timestamp = time()):
        self.block_id = block_id
        self.transaction_ids = transaction_ids
        self.version = version
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.difficulty_target = difficulty_target
        self.nonce = nonce

    @classmethod
    def genesis_block(cls):
        return Block(
            block_id = 1,
            transaction_ids = [],
            version = "1.1",
            previous_hash = 1,
            merkle_root = 1,
            difficulty_target = 10,
            nonce = 100
        )
