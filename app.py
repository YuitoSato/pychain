from flask import Flask, request

from app.controllers.block_controller import BlockController
from app.controllers.mining_controller import MiningController
from app.controllers.my_node_controller import MyNodeController
from app.controllers.node_controller import NodeController
from app.controllers.unconfirmed_transaction_controller import UnconfirmedTransactionController
from app.models.block import Block
from app.models.node import Node
from app.repositories.blockchain_repository import BlockchainRepository
from app.repositories.my_node_repository import MyNodeRepository
from app.repositories.node_repository import NodeRepository
from app.repositories.unconfirmed_transaction_repository import UnconfirmedTransactionRepository
from app.services.block_service import BlockService
from app.services.mining_service import MiningService
from app.services.my_node_service import MyNodeService
from app.services.node_service import NodeService
from app.services.unconfirmed_transaction_service import UnconfirmedTransactionService
from app.utils.hash_converter import HashConverter
from app.utils.pychain_encoder import PychainEncoder

app = Flask(__name__)
app.json_encoder = PychainEncoder

node_address = "node_address"
hash_converter = HashConverter(encoder = PychainEncoder)

my_node = Node(
    url = "localhost:5000",
    address = "yuito-node"
)

# Repositories
blockchain_repository = BlockchainRepository(genesis_block = Block.genesis_block())
unconfirmed_transaction_repository = UnconfirmedTransactionRepository()
my_node_repository = MyNodeRepository(node = my_node)
node_repository = NodeRepository()

# Services
mining_service = MiningService(
    unconfirmed_transaction_repository = unconfirmed_transaction_repository,
    blockchain_repository = blockchain_repository,
    my_node_repository = my_node_repository,
    hash_converter = hash_converter,
    node_address = node_address
)
unconfirmed_transaction_service = UnconfirmedTransactionService(
    unconfirmed_transaction_repository = unconfirmed_transaction_repository,
    blockchain_repository = blockchain_repository
)
block_service = BlockService(blockchain_repository = blockchain_repository)
my_node_service = MyNodeService(my_node_repository = my_node_repository)
node_service = NodeService(node_repository)

# Controllers
unconfirmed_transaction_controller = UnconfirmedTransactionController(
    unconfirmed_transaction_service = unconfirmed_transaction_service,
    hash_converter = hash_converter
)
mining_controller = MiningController(mining_service = mining_service)
block_controller = BlockController(block_service = block_service)
my_node_controller = MyNodeController(my_node_service = my_node_service)
node_controller = NodeController(node_service)


@app.route('/')
def hello_world():
    return 'Hello World!!!!'


@app.route('/transactions', methods = ['POST'])
def create_transaction():
    return unconfirmed_transaction_controller.create_transaction(request)


@app.route('/transactions/unconfirmed')
def list_current_transactions():
    return unconfirmed_transaction_controller.list_unconfirmed_transactions()


@app.route('/mine')
def mine():
    return mining_controller.mine()


@app.route('/blocks')
def list_blocks():
    return block_controller.list_blocks()


@app.route('/my-node', methods = ['POST'])
def update_my_node():
    return my_node_controller.update_my_node(request)


@app.route('/my-node')
def find_my_node():
    return my_node_controller.find_my_node()


@app.route('/nodes', methods = ['POST'])
def create_node():
    return node_controller.create_node(request)


app.run(host = '0.0.0.0', port = 5000)

# if __name__ == '__main__':
#     if sys.argv is not None and sys.argv[1] is not None:
#         app.run(host='0.0.0.0', port=int(sys.argv[1]))
#     else:
#         app.run(host='0.0.0.0', port=5000)
