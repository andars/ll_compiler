from lexer import Lexer
from parser import Parser
from tokens import Token

print("Parsing")
with open('tests/test.src') as f:
    lexer = Lexer(f)
    parser = Parser(lexer)
    parsed = parser.parse()

    for node in parsed:
        node.pprint(0)
