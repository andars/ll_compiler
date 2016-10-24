from .node import Node

class Global(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
