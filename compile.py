#!/usr/bin/env python3

import sys

from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator

with open("start.s", 'r') as rt:
    print(rt.read())

with open(sys.argv[1]) as f:
    lexer = Lexer(f)
    parser = Parser(lexer)
    parsed = parser.parse()
    codegen  = CodeGenerator()

    for node in parsed:
        codegen.codegen(node)
