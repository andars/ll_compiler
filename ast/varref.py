from .node import Node

class VarRef(Node):
    def __init__(self, vartype, index):
        self.vartype = vartype
        self.index = index
