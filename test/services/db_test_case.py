from unittest import TestCase

from app.database.sqlite import db
from app.model.block import Block
from app.model.transaction import Transaction
from app.model.transaction_output import TransactionOutput
from entrypoint import create_app


class DbTestCase(TestCase):
    @classmethod
    def seed(cls):
        timestamp = 0
        block = Block.build(
            block_number = 1,
            version = '1',
            previous_block_hash = '1',
            timestamp = 1,
            merkle_root = '',
            difficulty_target = 10,
            nonce = 1
        )
        transaction = Transaction.build(
            block_id = '1',
            locktime = 0,
            timestamp = timestamp
        )
        transaction_output = TransactionOutput.build(
            transaction_id = '1',
            amount = 10000000000000000000,
            sender_address = 'coinbase',
            recipient_address = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAznjoHvzCJtQcIYd3yj7v\ngwaPlyiG6U/Qlw1G89n0bNt5anvRe+e2eKzvpy98aj6ShGu7hARE9SxAFA9bIHCB\nqdAyPnrUaw7qGkeZNPHBByHe9prJSn0ZwBtfySOSbzdetO5aAwvLj5qMudW2PDz1\n5mP2taGOvXqNnbcH78ZHQLvF6G+SbwuLHU5LEDSZlcy+CnvPqD67cg+QmJLneVmQ\nfOBtbFHz3yDQghNrHWa+UCspUMHVGsDG6OEK7MSpPieY6TzBEYQWsikosQ+V0zBN\nrSCADe3GBcJ7XzafM/gb+gzJ1eP78F1sA6Ja4ZtqInqN406PwerAXaUJa2twW652\n9wIDAQAB\n-----END PUBLIC KEY-----',
            timestamp = timestamp
        )
        db.session.add(block)
        db.session.add(transaction)
        db.session.add(transaction_output)
        db.session.commit()

    def setUp(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.app_context().push()
        db.create_all()
        DbTestCase.seed()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
