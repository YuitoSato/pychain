from base64 import b64decode

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class TransactionInput:
    def __init__(self, transaction_input_id, transaction_id, transaction_output_id, amount, unlocking_script):
        self.transaction_input_id = transaction_input_id
        self.transaction_id = transaction_id
        self.transaction_output_id = transaction_output_id
        self.amount = amount
        self.unlocking_script = unlocking_script

    def verify(self, pubkey):
        rsakey = RSA.importKey(pubkey.encode('utf-8'))
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        output_id_str = str(self.transaction_output_id)
        data = output_id_str + ('/' * (-len(str(output_id_str)) % 4))
        digest.update(b64decode(data))

        return signer.verify(digest, b64decode(self.unlocking_script))
