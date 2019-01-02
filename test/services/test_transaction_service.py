from app.database.unconfirmed_transaction_pool import UnconfirmedTransactionPool
from app.services.transaction_service import TransactionService
from test.services.db_test_case import DbTestCase


class TestTransactionService(DbTestCase):
    def test_create_transaction(self):
        request = {
            'sender_address': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4JL8ek8HCgS6yvTSjog/\npfB7vc693fB1AA+8kBRchj51ktejPrR5mRpoMJwzBcgal9sAgLjj1gOa9pLReCfT\nRWuO+M0BiRJac1ebtAY5/A3dR52fE7U47/Agmm3qjL1Wqr3dbckrwgAHioA7RqhW\nqPQCl1m3qL66T9YlmvJxICzWX5+9ZQEcxSSyKT5gSBOoCWpE1aJlf8g6xoYSxRoT\nkES6AXDlYQh63eNeWIZXrOsf/0GEAlYxmLTh5QvNfIbN+Txck913ZP1DX8oQHJC4\nNKQNwAB+I0BovgJ71aFt3V7CeUN1+dYLbp/UcILfiZEyrbL1cRX6KHXH4HP/RTyj\nQwIDAQAB\n-----END PUBLIC KEY-----',
            'recipient_address': '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxnrb17FTtrgfg33ADcbc\nb2D7mGX+sBIn6jE24ADNKbAvqRuhonnBJxG5W21xMyfP43P4JS8Kb/e6MsdS0D5c\nwnvRmsgYZdCL9CvzMJ7gYGpaQ174S3ocdTveYVaMnnZExh8OCvfdGFs5O+wdBJF1\n1jhUmKaNAS45LWjYjou3db5oJdd87ISEHOmyB1UOp4bSIvF0EI5zHMS/kXE53t2W\n95PdsiXStj0HpzBp0C3jwzVLGDuyvALeC6ACg+9R6exBut8mjoDgL47m3/irFy0E\n2XEhmmRlpxH/hvFkGVvjMIEXBwdc+p1FDNQtGXEUkCWaBiQxNE+TE02qXlsQi6S+\nIwIDAQAB\n-----END PUBLIC KEY-----',
            'amount': 100,
            'transaction_inputs': [
                {
                    'transaction_output_id': 'd5b750651056f0f3f23eeda5187ef9e5e22be209e0921ca526957669d315c405',
                    'unlocking_script': '35pLa2XoKqIz0agLgeDchHtBg4nYaqJnK6jvwgBoHJyHIgnEnCSo4oo74lJIi48on5CZJLEo0mGCikG7JD4e7J4XhloJNMH4AmvPX5rftdp3yAJH6MPgAQnDDI0zx8gvls88xYzfZYFnUbFscmyKGd5Ehh3SQgjRghnrrykFCybkiwON0jH2rVB1C2xTsyJoaA840ykkl1WsM8NdMQwb4ukBjUP+NLbL6Fw2AH7LQcG/tTpNYSR+VujZoy/bXsaFpmcCtqDcJjvhvzY2vpVBunrm9T9A2ae0RlvuNKK3qbd9I1mAzhwpvWBdMUPInangrK9FjinLB1qEJPvNhC4OXQ=='
                }
            ],
            'timestamp': 0
        }

        TransactionService.create_transaction(request)

        self.assertEqual(len(UnconfirmedTransactionPool.transactions), 1)
