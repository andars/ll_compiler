export PATH := .:$(PATH)

SRCS := $(wildcard tests/*)
PROGS := $(SRCS:tests/%=build/%)
PROGS := $(PROGS:%.src=%)

.PHONY: test
test: $(PROGS)
	@run_tests

build/%: build/%.s
	as $? -o $@.o
	ld $@.o -o $@

build/%.s: tests/%.src *.py
	./compile.py $< > $@

.PHONY: clean
clean:
	rm build/*
