from .node import Node

class Alloc(Node):
    def __init__(self, count):
        self.count = count
