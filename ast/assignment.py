from .node import Node

class Assignment(Node):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
