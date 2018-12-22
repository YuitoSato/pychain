from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String, Float, Text

from app.infrastructure.rdb.sqlite.db_conf import DbConf


class Block(DbConf.Base):
    __tablename__ = "blocks"
    block_id = Column(BigInteger, primary_key = True, autoincrement = False)
    version = Column(String(length = 10), nullable = False)
    previous_block_hash = Column(String(length = 64), nullable = False)
    timestamp = Column(Integer, nullable = False)
    merkle_root = Column(String(length = 64), nullable = False)
    difficulty_target = Column(Integer, nullable = False)
    nonce = Column(Integer, nullable = False)


class Transaction(DbConf.Base):
    __tablename__ = 'transactions'
    transaction_id = Column(BigInteger, primary_key = True, autoincrement = False)
    input_counter = Column(Integer, nullable = False)
    output_counter = Column(Integer, nullable = False)
    locktime = Column(Integer, nullable = False)


class TransactionConfirmation(DbConf.Base):
    __tablename__ = "transaction_confirmations"
    transaction_confirmation_id = Column(BigInteger, primary_key = True, autoincrement = False)
    block_id = Column(BigInteger, ForeignKey('blocks.block_id'))
    transaction_id = Column(BigInteger, ForeignKey('transactions.transaction_id'))


class TransactionOutput(DbConf.Base):
    __tablename__ = "transaction_outputs"
    transaction_output_id = Column(BigInteger, primary_key = True, autoincrement = False)
    transaction_id = Column(BigInteger, ForeignKey('transactions.transaction_id'))
    amount = Column(Float(asdecimal = True), nullable = False)
    locking_script = Column(Text, nullable = False)
    sender_address = Column(String(length = 64), nullable = False)
    recipient_address = Column(String(length = 64), nullable = False)


class TransactionInputs(DbConf.Base):
    __tablename__ = "transaction_inputs"
    transaction_input_id = Column(BigInteger, primary_key = True, autoincrement = False)
    transaction_id = Column(BigInteger, ForeignKey('transactions.transaction_id'))
    transaction_output_id = Column(BigInteger, ForeignKey('transaction_outputs.transaction_output_id'))
    unlocking_script = Column(Text, nullable = False)


class PeerNode(DbConf.Base):
    __tablename__ = "peer_nodes"
    peer_node_id = Column(BigInteger, primary_key = True, autoincrement = False)
    url = Column(String(length = 64), nullable = False)
    address = Column(String(length = 64), nullable = False)


def main():
    DbConf.Base.metadata.create_all(bind = DbConf.ENGINE)


if __name__ == "__main__":
    main()
