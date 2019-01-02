import hashlib

from sqlalchemy import desc

from app.database.sqlite import db
from app.model.transaction import Transaction
from app.model.transaction_input import TransactionInput
from app.model.transaction_output import TransactionOutput


class Block(db.Model):
    __tablename__ = "blocks"
    block_id = db.Column(db.Text, primary_key = True, autoincrement = False)
    block_number = db.Column(db.Integer, nullable = False)
    version = db.Column(db.String(length = 10), nullable = False)
    previous_block_hash = db.Column(db.String(length = 64), nullable = False)
    timestamp = db.Column(db.Integer, nullable = False)
    merkle_root = db.Column(db.String(length = 64), nullable = False)
    difficulty_target = db.Column(db.Integer, nullable = False)
    nonce = db.Column(db.Integer, nullable = False)

    @classmethod
    def build(cls, block_number, version, previous_block_hash, timestamp, merkle_root, difficulty_target, nonce,
        transactions):
        return Block(
            block_id = hashlib.sha256((
                    version + previous_block_hash + str(timestamp) + merkle_root + str(difficulty_target) + str(
                    nonce)).encode('utf-8')).hexdigest(),
            block_number = block_number,
            version = version,
            previous_block_hash = previous_block_hash,
            timestamp = timestamp,
            merkle_root = merkle_root,
            difficulty_target = difficulty_target,
            nonce = nonce,
            transactions = transactions
        )

    @classmethod
    def list(cls):
        return cls.query \
            .outerjoin(Transaction, cls.block_id == Transaction.block_id) \
            .outerjoin(TransactionOutput, Transaction.transaction_id == TransactionOutput.transaction_id) \
            .outerjoin(TransactionInput, Transaction.transaction_id == TransactionInput.transaction_id) \
            .order_by(desc(cls.block_number)) \
            .all()

    @classmethod
    def last(cls):
        return cls.query.order_by(desc(cls.timestamp)).first()

    @classmethod
    def find(cls, block_id):
        return cls.query.filter(cls.block_id == block_id).first()

    @classmethod
    def create_block(cls, block):
        session = db.session
        session.add(block)
        session.add_all(block.transactions)

        for tx in block.transactions:
            session.add_all(tx.transaction_outputs)
            session.add_all(tx.transaction_inputs)

    @classmethod
    def find_by_block_number(cls, block_number):
        return cls.query \
            .outerjoin(Transaction, cls.block_id == Transaction.block_id) \
            .outerjoin(Transaction, TransactionOutput, Transaction.transaction_id == TransactionOutput.transaction_id) \
            .outerjoin(Transaction, TransactionInput, Transaction.transaction_id == TransactionInput.transaction_id) \
            .filter(cls.block_number == block_number).first()

    @classmethod
    def delete_blocks(cls, blocks):
        for block in blocks:
            db.session.delete(block)

    @classmethod
    def create_blocks(cls, blocks):
        for block in blocks:
            cls.create_block(block)
