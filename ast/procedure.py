from .node import Node

class Procedure(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
