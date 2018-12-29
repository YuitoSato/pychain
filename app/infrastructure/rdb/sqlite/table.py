from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String, Float, Text, LargeBinary

from app.infrastructure.rdb.sqlite.db_conf import DbConf
from app.models.transaction_output import TransactionOutput


class BlockRow(DbConf.Base):
    __tablename__ = "blocks"
    block_id = Column(BigInteger, primary_key = True, autoincrement = False)
    version = Column(String(length = 10), nullable = False)
    previous_block_hash = Column(String(length = 64), nullable = False)
    timestamp = Column(Integer, nullable = False)
    merkle_root = Column(String(length = 64), nullable = False)
    difficulty_target = Column(Integer, nullable = False)
    nonce = Column(Integer, nullable = False)


class TransactionRow(DbConf.Base):
    __tablename__ = 'transactions'
    transaction_id = Column(BigInteger, primary_key = True, autoincrement = False)
    locktime = Column(Integer, nullable = False)

    @classmethod
    def from_domain(cls, transaction):
        return TransactionRow(
            transaction_id = transaction.transaction_id,
            locktime = transaction.locktime
        )


class TransactionConfirmationRow(DbConf.Base):
    __tablename__ = "transaction_confirmations"
    transaction_confirmation_id = Column(BigInteger, primary_key = True, autoincrement = False)
    block_id = Column(BigInteger, ForeignKey('blocks.block_id'))
    transaction_id = Column(BigInteger, ForeignKey('transactions.transaction_id'))


class TransactionOutputRow(DbConf.Base):
    __tablename__ = "transaction_outputs"
    transaction_output_id = Column(BigInteger, primary_key = True, autoincrement = False)
    transaction_id = Column(BigInteger, ForeignKey('transactions.transaction_id'))
    amount = Column(Float(asdecimal = True), nullable = False)
    locking_script = Column(Text, nullable = False)
    sender_address = Column(Text, nullable = False)
    recipient_address = Column(Text, nullable = False)

    def to_domain(self):
        return TransactionOutput(
            transaction_output_id = self.transaction_output_id,
            transaction_id = self.transaction_id,
            amount = self.amount,
            locking_script = self.locking_script,
            sender_address = self.sender_address,
            recipient_address = self.recipient_address
        )

    @classmethod
    def from_domain(cls, transaction_output):
        return TransactionOutputRow(
            transaction_output_id = transaction_output.transaction_output_id,
            transaction_id = transaction_output.transaction_id,
            amount = transaction_output.amount,
            locking_script = transaction_output.locking_script,
            sender_address = transaction_output.sender_address,
            recipient_address = transaction_output.recipient_address
        )


class TransactionInputRow(DbConf.Base):
    __tablename__ = "transaction_inputs"
    transaction_input_id = Column(BigInteger, primary_key = True, autoincrement = False)
    transaction_id = Column(BigInteger, ForeignKey('transactions.transaction_id'))
    transaction_output_id = Column(BigInteger, ForeignKey('transaction_outputs.transaction_output_id'))
    unlocking_script = Column(Text, nullable = False)

    @classmethod
    def from_domain(cls, transaction_input):
        return TransactionInputRow(
            transaction_input_id = transaction_input.transaction_input_id,
            transaction_id = transaction_input.transaction_id,
            transaction_output_id = transaction_input.transaction_output_id,
            unlocking_script = transaction_input.unlocking_script
        )


class PeerNodeRow(DbConf.Base):
    __tablename__ = "peer_nodes"
    peer_node_id = Column(BigInteger, primary_key = True, autoincrement = False)
    url = Column(String(length = 64), nullable = False)
    address = Column(String(length = 64), nullable = False)


def main():
    DbConf.Base.metadata.create_all(bind = DbConf.ENGINE)


if __name__ == "__main__":
    main()
