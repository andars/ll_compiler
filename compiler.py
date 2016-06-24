class Compiler:
    def __init__(self, parsed):
        self.parsed = parsed
        self.enclosing = None

    def compile(self):
        for expr in self.parsed:
            self.compile_expr(expr)

    def compile_expr(self, expr):
        if expr[0] == 'procedure':
            self.compile_proc(expr)
        elif expr[0] == 'alloc':
            self.compile_alloc(expr)
        elif expr[0] == 'return':
            self.compile_return(expr)
        elif expr[0] == 'set':
            self.compile_set(expr)
        elif expr[0] in ['+', '-']:
            self.compile_operation(expr)
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
        self.compile_value(expr[1]) # place return value in %rax
        print("jmp " + self.enclosing + "_end") # jump to function epilogue

    def get_local_addr(self, expr):
        idx = expr[1] + 1
        offset = idx*8
        return "-" + str(offset) + "(%rbp)"

    def compile_set(self, expr):
        dst = expr[1]
        assert isinstance(dst, list) and dst[0] == 'local', "can only assign to variable"
        value = expr[2]
        self.compile_value(expr[2])
        print("mov %rax, " + self.get_local_addr(dst))

    # loads value indicated by expr into %rax
    def compile_value(self, expr):
        if isinstance(expr, int):
            print("mov $" + str(expr) + ", %rax")
        else:
            assert isinstance(expr, list), "unexpected value type {}".format(expr)
            if expr[0] == 'local':
                print("mov " + self.get_local_addr(expr) + ", %rax")
            else:
                self.compile_expr(expr)

    def compile_operation(self, expr):
        op = ''
        if expr[0] == '+':
            op = 'add'
        elif expr[0] == '-':
            op = 'sub'

        self.compile_value(expr[1]) # place first operand in %rax
        print("mov %rax, %rbx") # move first operand to %rbx
        self.compile_value(expr[2]) # place second operand in %rax

        print("{} %rbx, %rax".format(op))

    def output_label(self, label):
        print("{}:".format(label))
