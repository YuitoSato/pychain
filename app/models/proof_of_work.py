import hashlib

from app.models.proof_result import ProofResult


class ProofOfWork:
    max_nonce = 2 ** 32

    def __init__(self, header, difficulty_bits):
        self.header = header
        self.difficulty_bits = difficulty_bits

    def prove(self):
        nonce = 1
        target = 2 ** (256 - self.difficulty_bits)

        hash_result = 0

        print("Start proving")

        for nonce in range(ProofOfWork.max_nonce):
            hash_result = hashlib.sha256(str(self.header).encode('utf-8') + str(nonce).encode('utf-8')).hexdigest()
            proof_result = ProofResult(int(hash_result, 16), target, nonce)

            if proof_result.isValid():
                print("Success with nonce %d" % nonce)
                return proof_result

        print("Failed after %d (max_nonce) tries" % nonce)
        return ProofResult(int(hash_result, 16), target, nonce)
