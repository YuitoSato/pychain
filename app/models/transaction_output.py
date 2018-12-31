import uuid

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

from app.models.transaction_input import TransactionInput
from app.utils.constants import COINBASE_ADDRESS


class TransactionOutput:
    def __init__(self, transaction_output_id, transaction_id, amount, sender_address, recipient_address):
        self.transaction_output_id = transaction_output_id
        self.transaction_id = transaction_id
        self.amount = amount
        self.locking_script = TransactionOutput.calc_locking_script(recipient_address, transaction_output_id)
        self.sender_address = sender_address
        self.recipient_address = recipient_address

    def to_input(self, unlocking_script):
        return TransactionInput(
            transaction_input_id = uuid.uuid1().hex,
            transaction_id = self.transaction_id,
            transaction_output_id = self.transaction_output_id,
            amount = self.amount,
            unlocking_script = unlocking_script
        )

    @classmethod
    def calc_locking_script(cls, recipient_address, transaction_output_id):
        if recipient_address == COINBASE_ADDRESS:
            return COINBASE_ADDRESS
        else:
            public_key = RSA.importKey(recipient_address.encode('utf-8'))
            encryptor = PKCS1_OAEP.new(public_key, SHA256)
            encrypted = encryptor.encrypt(transaction_output_id.encode('utf-8'))
            return encrypted.decode('latin-1')
