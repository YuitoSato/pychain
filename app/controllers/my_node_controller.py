from flask.json import jsonify

from app.models.node import Node


class MyNodeController:
    def __init__(self, my_node_service):
        self.my_node_service = my_node_service

    def update_my_node(self, request):
        values = request.get_json()
        node = Node(url = request.host, address = values['address'])
        self.my_node_service.update_my_node(node)
        return jsonify({}), 200

    def find_my_node(self):
        node = self.my_node_service.find_my_node()
        return jsonify(node), 200
