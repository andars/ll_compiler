from tokens import Token

class Lexer:
    def __init__(self, f):
        self.file = f 
        self.offset = 0
        self.peeked = None

    def peek_token(self):
        if self.peeked:
            return self.peeked
        self.peeked = self.next_token()
        return self.peeked

    def next_token(self):
        if self.peeked:
            tok = self.peeked
            self.peeked = None
            return tok

        char = self.read_char()

        if char == '':
            return Token.EOF

        if char == ' ' or char == '\n' or char == '\t':
            return self.next_token()

        if char == '#':
            while self.read_char() != '\n':
                pass
            return self.next_token()

        if char == '(':
            return Token.OPEN_PAREN
        elif char == ')':
            return Token.CLOSE_PAREN
        elif char.isdigit():
            num = char
            while True:
                peeked = self.peek_char()
                if peeked in [' ', '\t', '\n', '', ')']:
                    break
                num += self.read_char()
                if not peeked.isdigit():
                    return self.read_symbol(num)
            return Token.NUM(int(num))
        else: 
            return self.read_symbol(char)

    def read_symbol(self, base):
        sym = base
        while True:
            peeked = self.peek_char()
            if peeked in [' ', '\t', '\n', '', ')']:
                break
            sym += self.read_char()
        return Token.SYMBOL(sym)

    # returns the next char and advances cursor
    def read_char(self):
        char = self.peek_char() 
        self.offset += 1
        return char
    
    # returns the next char to be read, doesn't advance cursor
    def peek_char(self):
        self.file.seek(self.offset)
        char = self.file.read(1)
        return char
    
