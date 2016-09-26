#!/usr/bin/env python3

import sys

from lexer import Lexer
from parser import Parser
from compiler import Compiler

with open(sys.argv[1]) as f:
    lexer = Lexer(f)
    parser = Parser(lexer)
    parsed = parser.parse()
    compiler = Compiler(parsed)
    compiler.compile()
