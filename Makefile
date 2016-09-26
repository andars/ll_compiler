.PHONY: run
run: build/test
	@./run $?
build/test: build/test.s
	as $? -o $@.o
	ld $@.o -o $@

build/test.s: test.txt *.py
	./compile.py $< > build/test.s

clean:
	rm build/*
