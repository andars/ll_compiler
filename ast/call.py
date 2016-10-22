from .node import Node

class Call(Node):
    def __init__(self, procedure, arguments):
        self.procedure = procedure
        self.arguments = arguments
