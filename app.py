from flask import Flask, request

from app.controllers.transaction_controller import TransactionController
from app.controllers.pychain_encorder import PychainEncorder
from app.models.block import Block
from app.stores.blockchain import Blockchain

app = Flask(__name__)
app.json_encoder = PychainEncorder

blockchain = Blockchain(Block.genesis_block())
transaction_controller = TransactionController(blockchain)


@app.route('/')
def hello_world():
    return 'Hello World!!!!'


@app.route('/transactions', methods=['POST'])
def create_transaction():
    return transaction_controller.create_transaction(request)


@app.route('/transactions/current')
def fetch_current_transactions():
    return transaction_controller.fetch_current_transactions()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
