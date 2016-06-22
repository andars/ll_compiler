import lex
from tokens import Token

with open('test.txt') as f:
    lexer = lex.Lexer(f)
    while True:
        if lexer.peek_token() == Token.EOF:
            break
        print(lexer.next_token())
