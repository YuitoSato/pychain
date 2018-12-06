import hashlib

from app.models.proof_result import ProofResult


class BlockService:
    def __init__(self, blockchain_repository, block_ws, node_repository, hash_converter):
        self.blockchain_repository = blockchain_repository
        self.block_ws = block_ws
        self.node_repository = node_repository
        self.hash_converter = hash_converter

    def list_blocks(self):
        return self.blockchain_repository.list_blocks()

    def find_last_block(self):
        return self.blockchain_repository.find_last_block()

    def verify_block(self, block_from_peer):
        hash_result = hashlib.sha256(
            str(block_from_peer.previous_hash).encode('utf-8') + str(block_from_peer.nonce).encode('utf-8')).hexdigest()
        proof_result = ProofResult(int(hash_result, 16), block_from_peer.difficulty, block_from_peer.nonce)
        if proof_result.isValid():
            last_block = self.blockchain_repository

            # 受信したブロックが次のブロックな時
            if self.hash_converter.hash(last_block) == block_from_peer.previous_hash:
                self.blockchain_repository.create_block(block_from_peer)
                nodes = self.node_repository.list_nodes()
                list(map(lambda node: self.block_ws.send_block(node, block_from_peer), nodes))
            else:
                self.resolve_conflict()

    def resolve_conflict(self):
        return
