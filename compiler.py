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
        if expr[0] == 'define':
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
        elif expr[0] == 'if':
            self.compile_if(expr)
        else:
            assert False, "unimplemented {}".format(expr)
    
    # compile a (define (<name> <param_count>) <stmts>) block
    def compile_proc(self, expr):
        name = expr[1][0]
        param_count = expr[1][1]

        self.enclosing = {
            'name': name,
            'local_count': 0,
            'param_count': param_count,
            'label_count': 0,
        }

        print(".globl " + name)
        self.output_label(name)

        # function prologue
        print("pushq %rbp")
        print("movq %rsp, %rbp")

        # allocate stack space for arguments & put them there
        print("subq ${}, %rsp".format(param_count * 8))
        for i in range(param_count):
            print("movq {}, {}".format(self.registers[i], self.get_param_addr(i)))

        body = expr[2:] # all remaining subexpressions after (procedure <name> <arg_count>...

        for expression in body:
            self.compile_expr(expression)

        # put a label at the end of the body, used for early returns
        self.output_label(name + "_end")

        # function epilogue
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

    def get_local_addr(self, local_number):
        assert 0 <= local_number and local_number < self.enclosing['local_count'], \
               "bad local index: {}".format(local_number)
        idx = local_number + 1 + self.enclosing['param_count']
        offset = idx*8
        return "-" + str(offset) + "(%rbp)"

    def get_param_addr(self, param_number):
        assert 0 <= param_number and param_number < self.enclosing['param_count'], \
                "bad param index: {}".format(param_number)
        idx = param_number + 1
        offset = idx * 8
        return "-" + str(offset) + "(%rbp)"

    def compile_set(self, expr):
        dst = expr[1]
        assert isinstance(dst, list) and dst[0] == 'local', "can only assign to variable"
        value = expr[2]
        self.compile_value(expr[2], '%rax')
        print("mov %rax, " + self.get_local_addr(dst[1]))

    # loads value indicated by expr into dest
    def compile_value(self, expr, dest):
        if isinstance(expr, int):
            print("mov $" + str(expr) + ", " + dest)
        else:
            assert isinstance(expr, list), "unexpected value type {}".format(expr)
            if expr[0] == 'local':
                print("mov " + self.get_local_addr(expr[1]) + ", " + dest)
            elif expr[0] == 'param':
                print("mov " + self.get_param_addr(expr[1]) + ", " + dest)
            else:
                self.compile_expr(expr)
                print("mov %rax, {}".format(dest))

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

        #TODO: push *only* the registers we need to stack
        # this is pretty bad but temporarily solves the problem 
        for reg in self.registers:
            print("pushq " + reg)

        for arg, reg in zip(args, self.registers):
            self.compile_value(arg, reg)
        print("callq {}".format(proc))

        # go back through registers and pop them off (in reverse)
        for reg in reversed(self.registers):
            print("popq " + reg)

    def compile_if(self, expr):
        cond = expr[1]
        if_branch = expr[2]
        else_branch = expr[3]

        else_label = "{}_{}_else".format(self.enclosing['name'], self.enclosing['label_count'])
        end_label = "{}_{}_end".format(self.enclosing['name'], self.enclosing['label_count'])

        self.compile_value(cond, '%rax')
        print("test %rax, %rax") # test condition
        print("je {}".format(else_label)) # if condition = 0, jump to else branch
        for expr in if_branch:
            self.compile_expr(expr)

        print("jmp {}".format(end_label))

        self.output_label(else_label)
        for expr in else_branch:
            self.compile_expr(expr)

        self.output_label(end_label)

    def output_label(self, label):
        print("{}:".format(label))
