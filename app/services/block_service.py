class BlockService:
    def __init__(self, blockchain_repository):
        self.blockchain_repository = blockchain_repository

    def list_blocks(self):
        return self.blockchain_repository.list_blocks()
