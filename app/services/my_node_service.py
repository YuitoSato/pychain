class MyNodeService:
    def __init__(self, my_node_repository):
        self.my_node_repository = my_node_repository

    def update_my_node(self, node):
        self.my_node_repository.update_my_node(node)

    def find_my_node(self):
        return self.my_node_repository.find_my_node()