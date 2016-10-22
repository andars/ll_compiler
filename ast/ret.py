from .node import Node

class Return(Node):
    def __init__(self, value):
        self.value = value
