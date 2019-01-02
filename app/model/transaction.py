import hashlib

from app.database.sqlite import db


class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Text, primary_key = True, autoincrement = False)
    block_id = db.Column(db.Text, db.ForeignKey('blocks.block_id'), nullable = False)
    locktime = db.Column(db.Integer, nullable = False)

    block = db.relationship('Block', backref = db.backref('transactions'), lazy = True)

    @classmethod
    def build(cls, block_id, locktime, timestamp):
        return Transaction(
            transaction_id = hashlib.sha256((str(locktime) + str(timestamp)).encode('utf-8')).hexdigest(),
            block_id = block_id,
            locktime = locktime
        )

    # @classmethod
    # def create_transaction(cls, transaction):
    #     db.session.add(transaction)
    #     for tx_input in transaction.transaction_inputs:
    #         db.session.add(tx_input)
    #     for tx_output in transaction.transaction_outputs:
    #         db.session.add(tx_output)

    @classmethod
    def find(cls, transaction_id):
        return Transaction.query.filter(cls.transaction_id == transaction_id).first()
