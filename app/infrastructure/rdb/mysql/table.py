from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.infrastructure.rdb.mysql.db_conf import DbConf


class Block(DbConf.Base):
    __tablename__ = "blocks"
    block_id = Column(BigInteger, primary_key = True, autoincrement = False)
    block_size = Column(Integer, nullable = False)
    transaction_counter = Column(Integer, nullable = False)

    block_headers = relationship("BlockHeader", backref = "blocks", order_by = "BlockHeader.block_header_id")


class BlockHeader(DbConf.Base):
    __tablename__ = 'block_headers'
    block_header_id = Column(BigInteger, primary_key = True, autoincrement = False)
    block_id = Column(ForeignKey('blocks.block_id'))
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


def main():
    DbConf.Base.metadata.create_all(bind = DbConf.ENGINE)


if __name__ == "__main__":
    main()
