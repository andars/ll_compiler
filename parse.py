from tokens import Token

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse_expr(self):
        print("parsing expr")
        if self.lexer.peek_token() == Token.EOF:
            raise SyntaxError("unexpected EOF")

        tok = self.lexer.peek_token()
        print(tok) 

        if tok == Token.OPEN_PAREN:
            self.lexer.next_token() # eat open paren
            tok_list = []
            while self.lexer.peek_token() != Token.CLOSE_PAREN:
                tok_list.append(self.parse_expr())
            self.lexer.next_token() # eat close paren
            return tok_list
        elif tok == Token.CLOSE_PAREN:
            raise SyntaxError("unexpected close paren")
        else:
            return self.parse_atom()

    def parse_atom(self):
        if self.lexer.peek_token() in [Token.SYMBOL, Token.NUM]:
            return self.lexer.next_token().data
        raise SyntaxError("unexpected atom" + str(self.lexer.peek_token()))

