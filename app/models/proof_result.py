class ProofResult:
    def __init__(self, result_hash_int, target_hash_int, nonce):
        self.result_hash_int = result_hash_int
        self.target_hash_int = target_hash_int
        self.nonce = nonce

    def isValid(self):
        return self.result_hash_int < self.target_hash_int
