class MyNodeService:
    def __init__(self, my_node_repository, node_ws):
        self.my_node_repository = my_node_repository
        self.node_ws = node_ws

    def update_my_node(self, node):
        self.my_node_repository.update_my_node(node)

    def find_my_node(self):
        return self.my_node_repository.find_my_node()

    def send_my_node(self):
        my_node = self.my_node_repository.find_my_node
        self.node_ws.send_node(my_node)
