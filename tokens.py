from enum import Enum
class Token(Enum):
    OPEN_PAREN = 1
    CLOSE_PAREN = 2
    SYMBOL = 3
    NUM = 4
    UNKNOWN = 5
    EOF = 6


    def __str__(self):
        s = "<" + str(self.name)
        if hasattr(self, 'data'):
            return s + ": " + str(self.data) + ">"
        return s + ">"
    

    def __call__(self, data):
        self.data = data
        return self
