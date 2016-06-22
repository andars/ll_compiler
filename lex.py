from tokens import Token

class Lexer:
    def __init__(self, f):
        self.file = f 
        self.offset = 0

    def next_token(self):
        char = self.read_char()

        if char == '':
            return Token.EOF

        if char == ' ' or char == '\n' or char == '\t':
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

    def read_char(self):
        char = self.peek_char() 
        self.offset += 1
        return char
    
    def peek_char(self):
        self.file.seek(self.offset)
        char = self.file.read(1)
        return char
    
