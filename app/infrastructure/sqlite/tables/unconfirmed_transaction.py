import sys

from sqlalchemy import Column, Float, String
from app.infrastructure.sqlite.db_conf import DbConf


class UnconfirmedTransaction(DbConf.Base):
    __tablename__ = 'unconfirmed_transactions'
    transaction_hash = Column('transaction_hash', String(length = 64, collation = 'utf8'))
    sender_address = Column('sender_address', String(length = 64, collation = 'utf8'))
    recipient_address = Column('recipient_address', String(length = 64, collation = 'utf8'))
    amount = Column('amount', Float(asdecimal = True))


def main(args):
    DbConf.Base.metadata.create_all(bind = DbConf.ENGINE)


if __name__ == "__main__":
    main(sys.argv)
