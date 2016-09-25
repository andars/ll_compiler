# Low-Level Language Compiler

The name needs some work.

This project is a exploratory compiler. 

It takes this as input (lots of parens, but *not* lisp):

```
(procedure main 
    (alloc 3)
    (set (local 0) (+ 5 2) )
    (set (local 1) (local 0))
    (set (local 2) (local 1))
    (set (local 2) (+ (local 1) 1))
    (return (local 2)))
```

And produces this as output (x86_64 assembly, linux):

```assembly
.globl _start
_start:
xor %rbp, %rbp
callq main
mov %rax, %rdi
mov $60, %rax
syscall

.globl main
main:
pushq %rbp
movq %rsp, %rbp
sub $24, %rsp
mov $2, %rbx
mov $5, %rax
add %rbx, %rax
mov %rax, -8(%rbp)
mov -8(%rbp), %rax
mov %rax, -16(%rbp)
mov -16(%rbp), %rax
mov %rax, -24(%rbp)
mov $1, %rbx
mov -16(%rbp), %rax
add %rbx, %rax
mov %rax, -24(%rbp)
mov -24(%rbp), %rax
jmp main_end
main_end:
mov %rbp, %rsp
pop %rbp
ret
```
