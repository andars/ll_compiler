from lexer import Lexer
from parser import Parser
from tokens import Token

print("Lexing:")
with open('lextest.txt') as f:
    lexer = Lexer(f)
    while True:
        if lexer.peek_token() == Token.EOF:
            break
        print(lexer.next_token())

print("Parsing")
with open('parsetest.txt') as f:
    lexer = Lexer(f)
    parser = Parser(lexer)
    print(parser.parse())
