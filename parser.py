from tokens import Token
from ast import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def expect(self, data):
        nt = self.lexer.next_token()
        if nt.data != data:
            raise SyntaxError("expected {} but got {}".format(data, nt.data))

    def parse(self):
        expressions = []
        while self.lexer.peek_token() != Token.EOF:
            expressions.append(self.parse_expr())
        return expressions

    def parse_expr(self):
        if self.lexer.peek_token() == Token.EOF:
            raise SyntaxError("unexpected EOF")

        tok = self.lexer.peek_token()

        #TODO: allow square brackets in place of parens?
        if tok == Token.OPEN_PAREN:
            self.lexer.next_token() # eat open paren
            tok_list = []

            peeked = self.lexer.peek_token()

            node = None


            if peeked == Token.SYMBOL:
                if peeked.data == 'define':
                    node = self.parse_procedure()
                elif peeked.data == 'set':
                    node = self.parse_assignment()
                elif peeked.data == 'alloc':
                    node = self.parse_alloc()
                elif peeked.data == 'param' or peeked.data == 'local':
                    node = self.parse_varref()
                elif peeked.data == 'if':
                    node = self.parse_conditional()
                elif peeked.data == 'return':
                    node = self.parse_return()
                else:
                    node = self.parse_binop()

            #while self.lexer.peek_token() != Token.CLOSE_PAREN:
            #    tok_list.append(self.parse_expr())
            self.lexer.next_token() # eat close paren
            return node
        elif tok == Token.CLOSE_PAREN:
            raise SyntaxError("unexpected close paren")
        else:
            return self.parse_atom()

    def parse_atom(self):
        if self.lexer.peek_token() in [Token.SYMBOL, Token.NUM]:
            return self.lexer.next_token().data
        raise SyntaxError("unexpected atom" + str(self.lexer.peek_token()))

    def parse_procedure(self):
        self.expect('define') # eat `define`
        self.lexer.next_token() # eat open paren
        name = self.parse_atom()
        params = self.parse_atom()
        self.lexer.next_token() # eat close paren

        body = []
        while self.lexer.peek_token() != Token.CLOSE_PAREN:
            body.append(self.parse_expr())

        return Procedure(name, params, body)

    def parse_assignment(self):
        self.expect('set') # eat `set`
        var = self.parse_expr()
        value = self.parse_expr()
        return Assignment(var, value)

    def parse_alloc(self):
        self.expect('alloc') # eat `alloc`
        count = self.parse_atom()
        return Alloc(count)

    def parse_varref(self):
        vartype = self.parse_atom() # `param` or `local`
        idx = self.parse_atom()
        return VarRef(vartype, idx)

    def parse_conditional(self):
        self.expect('if') # eat `if`
        cond = self.parse_expr()

        if_branch = []
        self.lexer.next_token() # eat open paren
        while self.lexer.peek_token() != Token.CLOSE_PAREN:
            if_branch.append(self.parse_expr())
        self.lexer.next_token() # eat close paren

        else_branch = []
        self.lexer.next_token() # eat open paren
        while self.lexer.peek_token() != Token.CLOSE_PAREN:
            else_branch.append(self.parse_expr())
        self.lexer.next_token() # eat close paren

        return Conditional(cond, if_branch, else_branch)

    def parse_return(self):
        self.expect('return') # eat `return`
        value = self.parse_expr()
        return Return(value)

    def parse_binop(self):
        operator = self.parse_atom()
        
        if operator in ['+', '-']:
            lhs = self.parse_expr()
            rhs = self.parse_expr()
            return BinOp(operator, lhs, rhs)
        else:
            args = []
            while self.lexer.peek_token() != Token.CLOSE_PAREN:
                args.append(self.parse_expr())
            return Call(operator, args)
