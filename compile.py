#!/usr/bin/env python3

from lexer import Lexer
from parser import Parser
from compiler import Compiler

with open('test.txt') as f:
    lexer = Lexer(f)
    parser = Parser(lexer)
    parsed = parser.parse()
    compiler = Compiler(parsed)
    compiler.compile()
