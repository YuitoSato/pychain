from unittest import TestCase

from app.infra.sqlite import TransactionDb, TransactionOutputDb
from app.infra.sqlite.database import db
from app.services.transaction_service import TransactionService
from entrypoint import create_app


class TestTransactionService(TestCase):
    @classmethod
    def seed(cls):
        transaction = TransactionDb(
            transaction_id = '1',
            locktime = 0
        )
        transaction_output = TransactionOutputDb(
            transaction_id = '1',
            transaction_output_id = '1',
            amount = 10000000000000000000,
            locking_script = 'àähIö9f&E½çÖ´]¸Í1ÁàäÎtjí+åãJó:ö»o\nÞL @ ÂÚrEk5\nhÛë\ntU£îj£])ÈÎdóá@Làâ*=a±§;q3x¤Üi<\¾t ÑÎy¥&e<\Ú÷OL%0þÌÔ ¡ud1û¨Fîu5tÞ¤`³î¯bpéÕt,1DÒ5nì4$\nÚê9\nÛåi    ÚLxDbµá\näºc <×ULí!Ý©LÏÜözNH¡³hÿc9\nÕõÚ²À(\nþ$?=G1I³¶çÄÈ\n',
            sender_address = 'coinbase',
            recipient_address = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAznjoHvzCJtQcIYd3yj7v\ngwaPlyiG6U/Qlw1G89n0bNt5anvRe+e2eKzvpy98aj6ShGu7hARE9SxAFA9bIHCB\nqdAyPnrUaw7qGkeZNPHBByHe9prJSn0ZwBtfySOSbzdetO5aAwvLj5qMudW2PDz1\n5mP2taGOvXqNnbcH78ZHQLvF6G+SbwuLHU5LEDSZlcy+CnvPqD67cg+QmJLneVmQ\nfOBtbFHz3yDQghNrHWa+UCspUMHVGsDG6OEK7MSpPieY6TzBEYQWsikosQ+V0zBN\nrSCADe3GBcJ7XzafM/gb+gzJ1eP78F1sA6Ja4ZtqInqN406PwerAXaUJa2twW652\n9wIDAQAB\n-----END PUBLIC KEY-----'
        )
        db.session.add(transaction)
        db.session.add(transaction_output)
        db.session.commit()

    def setUp(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.app_context().push()
        db.create_all()
        TestTransactionService.seed()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_transaction(self):
        request = {
            'sender_address': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4JL8ek8HCgS6yvTSjog/\npfB7vc693fB1AA+8kBRchj51ktejPrR5mRpoMJwzBcgal9sAgLjj1gOa9pLReCfT\nRWuO+M0BiRJac1ebtAY5/A3dR52fE7U47/Agmm3qjL1Wqr3dbckrwgAHioA7RqhW\nqPQCl1m3qL66T9YlmvJxICzWX5+9ZQEcxSSyKT5gSBOoCWpE1aJlf8g6xoYSxRoT\nkES6AXDlYQh63eNeWIZXrOsf/0GEAlYxmLTh5QvNfIbN+Txck913ZP1DX8oQHJC4\nNKQNwAB+I0BovgJ71aFt3V7CeUN1+dYLbp/UcILfiZEyrbL1cRX6KHXH4HP/RTyj\nQwIDAQAB\n-----END PUBLIC KEY-----',
            'recipient_address': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxnrb17FTtrgfg33ADcbc\nb2D7mGX+sBIn6jE24ADNKbAvqRuhonnBJxG5W21xMyfP43P4JS8Kb/e6MsdS0D5c\nwnvRmsgYZdCL9CvzMJ7gYGpaQ174S3ocdTveYVaMnnZExh8OCvfdGFs5O+wdBJF1\n1jhUmKaNAS45LWjYjou3db5oJdd87ISEHOmyB1UOp4bSIvF0EI5zHMS/kXE53t2W\n95PdsiXStj0HpzBp0C3jwzVLGDuyvALeC6ACg+9R6exBut8mjoDgL47m3/irFy0E\n2XEhmmRlpxH/hvFkGVvjMIEXBwdc+p1FDNQtGXEUkCWaBiQxNE+TE02qXlsQi6S+\nIwIDAQAB\n-----END PUBLIC KEY-----',
            'amount': 100,
            'transaction_inputs': [
                {
                    'transaction_output_id': 1,
                    'unlocking_script': "JMIyAbhkmPM2OqYxoXxGPUjrLCFU7ypjhHTgQWZ/MZz43YpttI2WLheNyqmfStkJitsShWtSBqoGzCKOEScH0i4tlA1ATVU8sf6PKY1+FaDxBGAfbm44Nz3YD3/ZTXEDrFAN+kSVwYNOLokNdzkOZ83PKSJ1ugpftHe9Lu6JJdrEDG9wY29kccGBWBBTKOsxlFlLo144SVmi0bObF8GFdh5LvF1bX0Z5uq4dD7IrYd+7J9iISd9LAgA1ZAmzRw3zWMfbvYZyH8kDhxSbdeP95IrqTa0qVBoWx22Wb6LGLDd5K2tBUjJ78SdSER/sry3YKBNlzE13+wz9XvvaNtgSIQ=="
                }
            ]
        }

        TransactionService.create_transaction(request)

        results = TransactionOutputDb.list(db.session)
        self.assertEqual(len(results), 4)
