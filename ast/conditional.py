from .node import Node

class Conditional(Node):
    def __init__(self, cond, if_branch, else_branch):
        self.condition = cond
        self.if_branch = if_branch
        self.else_branch = else_branch
