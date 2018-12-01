class MyNodeRepository:
    def __init__(self, node):
        self.my_node = node

    def update_my_node(self, node):
        self.my_node = node

    def find_my_node(self):
        return self.my_node
