from flask.json import jsonify

from app.models.node import Node


class NodeController:
    def __init__(self, node_service):
        self.node_service = node_service

    def create_node(self, request):
        values = request.get_json()
        node = Node(
            url = values['url'],
            address = values['address']
        )
        self.node_service.create_node(node)
        return jsonify({}), 201
