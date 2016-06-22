from tokens import Token
from lexer import Lexer

with open('lextest.txt') as f:
    lexer = Lexer(f)
    while True:
        if lexer.peek_token() == Token.EOF:
            break
        print(lexer.next_token())
