.PHONY: run
run: build/test
	@./run $?
build/test: build/test.s
	as $? -o $@.o
	ld $@.o -o $@

build/test.s: *.py test.txt
	./compile.py > build/test.s

clean:
	rm build/*
