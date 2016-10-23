from ast import *
import sys
from io import StringIO

def _qualified_name(obj):
    return obj.__module__ + '.' + obj.__qualname__

def _declaring_class(obj):
    name = _qualified_name(obj)
    return name[: name.rfind('.')]

_methods = {}

def _impl(self, arg):
    method = _methods[(_qualified_name(type(self)), type(arg))]
    return method(self, arg)

def when(nodetype):
    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, nodetype)] = fn
        return _impl
    return decorator

class CodeGenerator():
    def __init__(self, output_file=sys.stdout):
        self.output_file = output_file
        self.registers = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"]
        self.buffers = []
        self.buffer = output_file

    def debug(self, *args):
        print(*args, file=sys.stderr)

    def emit(self, *args, **kwargs):
        print(*args, file=self.buffer, **kwargs)

    def emit_label(self, label):
        self.enclosing['label_count'] += 1
        self.emit("{}:".format(label))

    @when(BinOp)
    def codegen(self, node):
        if node.op == '+':
            op = "addq"
        elif node.op == '-':
            op = "subq"

        self.codegen(node.rhs)
        self.emit("movq %rax, %rbx")
        self.codegen(node.lhs)
        self.emit("{} %rbx, %rax".format(op))

    @when(Procedure)
    def codegen(self, node):
        name = node.name
        param_count = node.params

        self.enclosing = {
                'name': name,
                'local_count': 0,
                'param_count': param_count,
                'label_count': 0,
                }

        self.emit(".globl {}".format(name))
        self.emit_label(name)
        self.emit("pushq %rbp")
        self.emit("movq %rsp, %rbp")

        # copy arguments to storage on the stack
        self.emit("subq ${}, %rsp".format(param_count*8))
        for i in range(param_count):
            addr = self.address(VarRef('param', i))
            self.emit("movq {}, {}".format(self.registers[i], addr))

        for n in node.body:
            self.codegen(n)

        self.emit_label("{}_end".format(name))

        self.emit("movq %rbp, %rsp")
        self.emit("pop %rbp")
        self.emit("ret\n")
        self.enclosing = None

    @when(VarRef)
    def codegen(self, node):
        address = self.address(node)
        self.emit("movq {}, %rax # variable".format(address))

    @when(Alloc)
    def codegen(self, node):
        count = node.count
        self.enclosing['local_count'] += count
        self.emit("subq ${}, %rsp".format(count * 8))

    @when(Return)
    def codegen(self, node):
        self.codegen(node.value)
        self.emit("jmp {}_end # returning".format(self.enclosing['name']))

    @when(Assignment)
    def codegen(self, node):
        var = node.variable
        self.codegen(node.value)
        self.emit("movq %rax, {}".format(self.address(var)))

    @when(Conditional)
    def codegen(self, node):
        cond = node.condition
        label_base = "{}_{}".format(self.enclosing['name'],
                                    self.enclosing['label_count'])

        else_label = label_base + "_else"
        end_label = label_base + "_end"

        self.codegen(cond)
        self.emit("test %rax, %rax")
        self.emit("je {}".format(else_label))

        for child_node in node.if_branch:
            self.codegen(child_node)

        self.emit("jmp {}".format(end_label))

        self.emit_label(else_label)
        for child_node in node.else_branch:
            self.codegen(child_node)

        self.emit_label(end_label)

    @when(Call)
    def codegen(self, node):
        for i in range(len(node.arguments)):
            self.emit("pushq {}".format(self.registers[i]))

        for arg, reg in zip(node.arguments, self.registers):
            self.codegen(arg)
            self.emit("movq %rax, {}".format(reg))

        self.emit("callq {}".format(node.procedure))

        for i in reversed(range(len(node.arguments))):
            self.emit("popq {}".format(self.registers[i]))

    @when(int)
    def codegen(self, node):
        self.emit("movq ${}, %rax".format(node))

    def address(self, node):
        if node.vartype == "local":
            offset = node.index + 1 + self.enclosing['param_count']
        elif node.vartype == "param":
            offset = node.index + 1
        return "-{}(%rbp)".format(offset*8)
