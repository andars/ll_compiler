from lexer import Lexer
from parser import Parser
from tokens import Token

print("Parsing")
with open('parsetest.txt') as f:
    lexer = Lexer(f)
    parser = Parser(lexer)
    print(parser.parse())
