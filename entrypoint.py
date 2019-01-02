import sys
import uuid

from flask import Flask, request

from app.controllers.block_controller import BlockController
from app.controllers.transaction_controller import TransactionController
from app.database.sqlite import init_db
from app.models.peer_node import PeerNode
from app.utils.pychain_encoder import PychainEncoder


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('app/conf/config.py')

    init_db(app)
    app.json_encoder = PychainEncoder

    return app


app = create_app()

my_node = PeerNode(
    peer_node_id = uuid.uuid1().int,
    url = "localhost:5000",
    address = "yuito-node"
)


@app.route('/')
def hello_world():
    return 'Hello World!!!!'


@app.route('/transactions', methods = ['POST'])
def create_transaction():
    return TransactionController.create_transaction(request)


@app.route('/transactions/receive', methods = ['POST'])
def receive_transaction():
    return TransactionController.receive_transaction(request)


@app.route('/transactions/unconfirmed')
def list_current_transactions():
    return TransactionController.list_unconfirmed()


@app.route('/blocks/mine')
def create_block():
    return BlockController.create_block()


@app.route('/blocks/receive', methods = ['POST'])
def receive_block():
    return BlockController.receive_block(request)


@app.route('/blocks')
def list_blocks():
    return BlockController.list_blocks()


@app.route('/blocks/<block_number>')
def find_by_block_number(block_number):
    return BlockController.find_by_block_number(block_number)


#
# @app.route('/my-node', methods = ['POST'])
# def update_my_node():
#     return my_node_controller.update_my_node(request)
#
#
# @app.route('/my-node')
# def find_my_node():
#     return my_node_controller.find_my_node()
#
#
# @app.route('/nodes', methods = ['POST'])
# def create_node():
#     return node_controller.create_node(request)
#
#
# @app.route('/nodes')
# def list_nodes():
#     return node_controller.list_nodes()


if __name__ == '__main__':
    if sys.argv is not None and sys.argv[1] is not None:
        port = int(sys.argv[1])
        app.run(host = '0.0.0.0', port = port)
    else:
        port = int(sys.argv[1])
        app.run(host = '0.0.0.0', port = 5000)

    print(app.config.from_pyfile('instance/config.py')['HOGE'])
