from flask import Flask, request

from app.controllers.block_controller import BlockController
from app.controllers.mining_controller import MiningController
from app.controllers.transaction_controller import TransactionController
from app.utils.hash_converter import HashConverter
from app.utils.pychain_encoder import PychainEncoder
from app.models.block import Block
from app.stores.blockchain import Blockchain

app = Flask(__name__)
app.json_encoder = PychainEncoder

blockchain = Blockchain(Block.genesis_block())
node_address = "node_address"
hash_converter = HashConverter(PychainEncoder)

transaction_controller = TransactionController(blockchain, hash_converter)
mining_controller = MiningController(blockchain, node_address, hash_converter)
block_controller = BlockController(blockchain)


@app.route('/')
def hello_world():
    return 'Hello World!!!!'


@app.route('/transactions', methods=['POST'])
def create_transaction():
    return transaction_controller.create_transaction(request)


@app.route('/transactions/current')
def fetch_current_transactions():
    return transaction_controller.fetch_current_transactions()


@app.route('/mine')
def mine():
    return mining_controller.mine()


@app.route('/blocks')
def fetch_blocks():
    return block_controller.fetch_blocks()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
