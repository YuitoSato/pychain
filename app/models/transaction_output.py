import hashlib
import uuid

from app.database.sqlite import db
from app.models.transaction_input import TransactionInput
from app.utils.constants import COINBASE_ADDRESS
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


class TransactionOutput(db.Model):
    __tablename__ = "transaction_outputs"
    transaction_output_id = db.Column(db.Text, primary_key = True, autoincrement = False)
    transaction_id = db.Column(db.Text, db.ForeignKey('transactions.transaction_id'))
    amount = db.Column(db.Float(asdecimal = True), nullable = False)
    locking_script = db.Column(db.Text, nullable = False)
    sender_address = db.Column(db.Text, nullable = False)
    recipient_address = db.Column(db.Text, nullable = False)

    transaction = db.relationship('Transaction', backref = db.backref('transaction_outputs'), lazy = True)

    @classmethod
    def build(cls, transaction_id, amount, sender_address, recipient_address, timestamp):
        transaction_output_id = hashlib.sha256((transaction_id + str(amount) + sender_address + recipient_address + str(timestamp)).encode('utf-8')).hexdigest()

        return TransactionOutput(
            transaction_output_id = transaction_output_id,
            transaction_id = transaction_id,
            amount = amount,
            locking_script = TransactionOutput.calc_locking_script(recipient_address, transaction_output_id),
            sender_address = sender_address,
            recipient_address = recipient_address
        )

    def to_input(self, unlocking_script):
        return TransactionInput(
            transaction_input_id = uuid.uuid1().hex,
            transaction_id = self.transaction_id,
            transaction_output_id = self.transaction_output_id,
            unlocking_script = unlocking_script,
            transaction_output = self
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

    @classmethod
    def find(cls, transaction_output_id):
        return cls.query \
            .filter(cls.transaction_output_id == transaction_output_id) \
            .first()

    @classmethod
    def find_unspent(cls, transaction_output_id):
        db_model = cls.query \
            .outerjoin(TransactionInput, cls.transaction_output_id == TransactionInput.transaction_output_id) \
            .filter(cls.transaction_output_id == transaction_output_id) \
            .first()

        if len(db_model.transaction_inputs) > 1:
            return None

        return db_model

    @classmethod
    def list_unspent(cls, address):
        return cls.query \
            .filter(cls.recipient_address == address) \
            .all()

    @classmethod
    def list(cls) -> object:
        return cls.query.all()
