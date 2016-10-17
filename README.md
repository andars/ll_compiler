# Low-Level Language Compiler

The name needs some work.

This project is a exploratory compiler. 


### Fibonacci

First argument to `fib` is index

```
(define (fib 3)
    (if (param 0)
        ((return (call fib ((- (param 0) 1) (param 2) (+ (param 1) (param 2))))))
        ((return (param 1)))))

(define (main 0)
    (alloc 2)
    (set (local 0) 0)
    (return (call fib (5 1 1))))
```

### Another Example

It takes this as input (lots of parens, but *not* currently a lisp):

```
(define (foo 1)
    (alloc 1)
    (return (param 0)))

(define (main 0)
    (alloc 3)
    (set (local 0) (+ 5 2) )
    (set (local 1) (local 0))
    (set (local 2) (local 1))
    (set (local 2) (+ (local 1) 1))
    (set (local 0) (call foo (27)))
    (set (local 1) (call foo (28)))
    (set (local 1) (+ (local 0) (local 1)))
    (return (local 1)))
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

.globl foo
foo:
pushq %rbp
movq %rsp, %rbp
sub $8, %rsp
mov %rdi, %rax
jmp foo_end
foo_end:
mov %rbp, %rsp
pop %rbp
ret

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
mov $27, %rdi
callq foo
mov %rax, -8(%rbp)
mov $28, %rdi
callq foo
mov %rax, -16(%rbp)
mov -16(%rbp), %rbx
mov -8(%rbp), %rax
add %rbx, %rax
mov %rax, -16(%rbp)
mov -16(%rbp), %rax
jmp main_end
main_end:
mov %rbp, %rsp
pop %rbp
ret
```
