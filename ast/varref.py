from .node import Node

class VarRef(Node):
    def __init__(self, vartype, index):
        self.vartype = vartype
        self.index = index

        # kluge support for named globals for now
        # will be fixed once parameters and locals get names
        self.name = index

