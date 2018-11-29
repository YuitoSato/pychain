from flask import Flask, request

from app.controllers.block_controller import BlockController
from app.controllers.mining_controller import MiningController
from app.controllers.unconfirmed_transaction_controller import UnconfirmedTransactionController
from app.repositories.blockchain_repository import BlockchainRepository
from app.repositories.unconfirmed_transaction_repository import UnconfirmedTransactionRepository
from app.services.mining_service import MiningService
from app.services.unconfirmed_transaction_service import UnconfirmedTransactionService
from app.utils.hash_converter import HashConverter
from app.utils.pychain_encoder import PychainEncoder
from app.models.block import Block
from app.stores.blockchain import Blockchain
from app.stores.unconfirmed_transaction_store import UnconfirmedTransactionStore

app = Flask(__name__)
app.json_encoder = PychainEncoder

blockchain = Blockchain(Block.genesis_block())
unconfirmed_transaction_store = UnconfirmedTransactionStore()

node_address = "node_address"
hash_converter = HashConverter(encoder = PychainEncoder)

# Repositories
blockchain_repository = BlockchainRepository(genesis_block = Block.genesis_block())
unconfirmed_transaction_repository = UnconfirmedTransactionRepository()

# Services
mining_service = MiningService(
    unconfirmed_transaction_repository = unconfirmed_transaction_repository,
    blockchain_repository = blockchain_repository,
    hash_converter = hash_converter,
    node_address = node_address
)
unconfirmed_transaction_service = UnconfirmedTransactionService(
    unconfirmed_transaction_repository = unconfirmed_transaction_repository,
    blockchain_repository = blockchain_repository
)

# Controllers
unconfirmed_transaction_controller = UnconfirmedTransactionController(
    unconfirmed_transaction_service = unconfirmed_transaction_service,
    hash_converter = hash_converter
)
mining_controller = MiningController(mining_service = mining_service)
# block_controller = BlockController(blockchain)

@app.route('/')
def hello_world():
    return 'Hello World!!!!'


@app.route('/transactions', methods=['POST'])
def create_transaction():
    return unconfirmed_transaction_controller.create_transaction(request)


@app.route('/transactions/current')
def fetch_current_transactions():
    return unconfirmed_transaction_controller.list_unconfirmed_transactions()


@app.route('/mine')
def mine():
    return mining_controller.mine()


# @app.route('/blocks')
# def fetch_blocks():
    # return block_controller.fetch_blocks()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
