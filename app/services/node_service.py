class NodeService:
    def __init__(self, node_repository):
        self.node_repository = node_repository

    def create_node(self, node):
        self.node_repository.create_node(node)