import lex
import parse
from tokens import Token

print("Lexing:")
with open('lextest.txt') as f:
    lexer = lex.Lexer(f)
    while True:
        if lexer.peek_token() == Token.EOF:
            break
        print(lexer.next_token())

print("Parsing")
with open('parsetest.txt') as f:
    lexer = lex.Lexer(f)
    parser = parse.Parser(lexer)
    print(parser.parse_expr())
