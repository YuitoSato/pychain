class BlockchainRepository:
    def __init__(self, genesis_block):
        self.blocks = [genesis_block]

    def create_block(self, block):
        self.blocks.append(block)

    def find_last_block(self):
        return self.blocks[-1]

    def list_blocks(self):
        return self.blocks
