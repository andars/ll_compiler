class Compiler:
    def __init__(self, parsed):
        self.parsed = parsed

    def compile(self):
        for expr in self.parsed:
            self.compile_expr(expr)

    def compile_expr(self, expr):
        if expr[0] == 'procedure':
            self.compile_proc(expr)
        elif expr[0] == 'alloc':
            self.compile_alloc(expr)
        else:
            assert False, "unimplemented {}".format(expr)
    
    #compile a (procedure <name> <stmts>) block
    def compile_proc(self, expr):
        name = expr[1]
        
        self.output_label(name)
        print("pushq %rbp")
        print("movq %rsp, %rbp")

        body = expr[2:-1] # all remaining subexpressions after (procedure <name> ...

        for expression in body:
            self.compile_expr(expression)

        print("mov %rbp, %rsp")
        print("pop %rbp")
        print("ret")

    def compile_alloc(self, expr):
        assert len(expr) == 2, "bad alloc syntax" # TODO: make sema for this stuff
        print("sub ${}, %rsp".format(expr[1] * 8))

    def output_label(self, label):
        print("{}:".format(label))


