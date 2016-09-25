.globl _start
_start:
xor %rbp, %rbp
callq main
mov %rax, %rdi
mov $60, %rax
syscall
