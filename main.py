import lex
from tokens import Token

with open('test.txt') as f:
    lexer = lex.Lexer(f)
    while True:
        tok = lexer.next_token()
        if tok == Token.EOF:
            break
        print(tok)
