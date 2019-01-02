from flask.json import jsonify

from app.models.peer_node import PeerNode


class NodeController:
    def create_node(self, request):
        values = request.get_json()
        node = PeerNode(
            url = values['url'],
            address = values['address']
        )
        self.node_service.create_node(node)
        return jsonify({}), 201

    def receive_node(self, request):
        values = request.get_json()
        node = PeerNode(
            url = request.host,
            address = values['address']
        )
        self.node_service.create_node(node)
        return jsonify({}), 201
