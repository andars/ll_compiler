class Compiler:
    def __init__(self, parsed):
        self.parsed = parsed
        self.enclosing = None

    def compile(self):
        for expr in self.parsed:
            self.compile_expr(expr)

    def compile_expr(self, expr):
        if isinstance(expr, int):
            print("$" + str(expr), end='')
        elif expr[0] == 'procedure':
            self.compile_proc(expr)
        elif expr[0] == 'alloc':
            self.compile_alloc(expr)
        elif expr[0] == 'return':
            self.compile_return(expr)
        elif expr[0] == 'local':
            self.compile_local(expr)
        elif expr[0] == 'set':
            self.compile_set(expr)
        else:
            assert False, "unimplemented {}".format(expr)
    
    #compile a (procedure <name> <stmts>) block
    def compile_proc(self, expr):
        name = expr[1]
        self.enclosing = name
        
        print(".globl " + name)
        self.output_label(name)
        print("pushq %rbp")
        print("movq %rsp, %rbp")

        body = expr[2:] # all remaining subexpressions after (procedure <name> ...

        for expression in body:
            self.compile_expr(expression)

        self.output_label(name + "_end")
        print("mov %rbp, %rsp")
        print("pop %rbp")
        print("ret")

        self.enclosing = None

    # compile an (alloc <count>) expression
    def compile_alloc(self, expr):
        assert len(expr) == 2, "bad alloc syntax" # TODO: make sema for this stuff
        print("sub ${}, %rsp".format(expr[1] * 8))

    # compile a (return <value>) expression
    def compile_return(self, expr):
        print("movq ", end='')
        self.compile_expr(expr[1])
        print(", %rax") # place return value in %rax
        print("jmp " + self.enclosing + "_end") # jump to function epilogue

    def compile_local(self, expr):
        idx = expr[1] + 1
        offset = idx*8
        print("-" + str(offset) + "(%rbp)", end="")

    def compile_set(self, expr):
        dst = expr[1]
        print("movq ", end='')
        self.compile_expr(expr[2])
        print(", ", end='')
        self.compile_expr(dst)
        print()


    def output_label(self, label):
        print("{}:".format(label))
