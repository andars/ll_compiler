.PHONY: run
run: build/test
	@./run $?
build/test: build/test.s
	as $? -o $@.o
	ld $@.o -o $@

build/test.s:
	./compile.py > build/test.s
