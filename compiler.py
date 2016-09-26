class Compiler:
    def __init__(self, parsed):
        self.parsed = parsed
        self.enclosing = None
        self.registers = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]

    def compile(self):
        with open('start.s', 'r') as start_file:
            print(start_file.read())
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
        elif expr[0] == 'call':
            self.compile_call(expr)
        else:
            assert False, "unimplemented {}".format(expr)
    
    #compile a (procedure <name> <stmts>) block
    def compile_proc(self, expr):
        name = expr[1]
        param_count = expr[2]

        self.enclosing = {
            'name': name,
            'local_count': 0,
            'param_count' : param_count,
        }

        print(".globl " + name)
        self.output_label(name)
        print("pushq %rbp")
        print("movq %rsp, %rbp")

        body = expr[3:] # all remaining subexpressions after (procedure <name> ...

        for expression in body:
            self.compile_expr(expression)

        self.output_label(name + "_end")
        print("mov %rbp, %rsp")
        print("pop %rbp")
        print("ret\n")

        self.enclosing = None

    # compile an (alloc <count>) expression
    def compile_alloc(self, expr):
        assert len(expr) == 2, "bad alloc syntax" # TODO: make sema for this stuff
        count = expr[1]
        self.enclosing['local_count'] += count
        print("sub ${}, %rsp".format(count * 8))

    # compile a (return <value>) expression
    def compile_return(self, expr):
        self.compile_value(expr[1], '%rax') # place return value in %rax
        print("jmp " + self.enclosing['name'] + "_end") # jump to function epilogue

    def get_local_addr(self, expr):
        assert 0 <= expr[1] and expr[1] < self.enclosing['local_count'], \
               "bad local index: {}".format(expr[1])
        idx = expr[1] + 1
        offset = idx*8
        return "-" + str(offset) + "(%rbp)"

    def get_param_location(self, expr):
        param_number = expr[1]
        assert 0 <= param_number and param_number < self.enclosing['param_count'], \
                "bad param index: {}".format(param_number)
        reg = self.registers[param_number]
        return reg

    def compile_set(self, expr):
        dst = expr[1]
        assert isinstance(dst, list) and dst[0] == 'local', "can only assign to variable"
        value = expr[2]
        self.compile_value(expr[2], '%rax')
        print("mov %rax, " + self.get_local_addr(dst))

    # loads value indicated by expr into dest
    def compile_value(self, expr, dest):
        if isinstance(expr, int):
            print("mov $" + str(expr) + ", " + dest)
        else:
            assert isinstance(expr, list), "unexpected value type {}".format(expr)
            if expr[0] == 'local':
                print("mov " + self.get_local_addr(expr) + ", " + dest)
            elif expr[0] == 'param':
                print("mov " + self.get_param_location(expr) + ", " + dest)
            else:
                self.compile_expr(expr)

    def compile_operation(self, expr):
        op = ''
        if expr[0] == '+':
            op = 'add'
        elif expr[0] == '-':
            op = 'sub'

        self.compile_value(expr[2], '%rbx') # place first operand in %rax
        self.compile_value(expr[1], '%rax') # place second operand in %rax

        print("{} %rbx, %rax".format(op))

    #compile (call <name> <args>) 
    def compile_call(self, expr):
        proc = expr[1]
        args = expr[2]

        #TODO: push all the registers we need (esp. current function's arguments) to stack

        for arg, reg in zip(args, self.registers):
            self.compile_value(arg, reg)
        print("callq {}".format(proc))

    def output_label(self, label):
        print("{}:".format(label))
