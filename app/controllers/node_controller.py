from flask.json import jsonify

from app.models.node import Node


class NodeController:
    def __init__(self, node_service):
        self.node_service = node_service

    def list_nodes(self):
        nodes = self.node_service.list_nodes()
        return jsonify(nodes), 200

    def create_node(self, request):
        values = request.get_json()
        node = Node(
            url = values['url'],
            address = values['address']
        )
        self.node_service.create_node(node)
        return jsonify({}), 201

    def receive_node(self, request):
        values = request.get_json()
        node = Node(
            url = request.host,
            address = values['address']
        )
        self.node_service.create_node(node)
        return jsonify({}), 201
