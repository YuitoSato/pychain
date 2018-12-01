class NodeRepository:
    def __init__(self):
        self.nodes = []

    def create_node(self, node):
        self.nodes.append(node)

    def list_nodes(self):
        return self.nodes
