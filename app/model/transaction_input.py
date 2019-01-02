from app.database.sqlite import db
from base64 import b64decode
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class TransactionInput(db.Model):
    __tablename__ = "transaction_inputs"
    transaction_input_id = db.Column(db.Text, primary_key = True, autoincrement = False)
    transaction_id = db.Column(db.Text, db.ForeignKey('transactions.transaction_id'), nullable = False)
    transaction_output_id = db.Column(db.Text, db.ForeignKey('transaction_outputs.transaction_output_id'), nullable = False)
    unlocking_script = db.Column(db.Text, nullable = False)

    transaction = db.relationship('Transaction', backref = db.backref('transaction_inputs'), lazy = True)
    transaction_output = db.relationship('TransactionOutput', backref = db.backref('transaction_inputs', lazy=True))

    def verify(self, pubkey):
        rsakey = RSA.importKey(pubkey.encode('utf-8'))
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        output_id_str = str(self.transaction_output_id)
        data = output_id_str + ('/' * (-len(str(output_id_str)) % 4))
        digest.update(b64decode(data))

        return signer.verify(digest, b64decode(self.unlocking_script))
