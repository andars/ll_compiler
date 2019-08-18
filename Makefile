export PATH := .:$(PATH)

SRC_FILES := $(wildcard tests/*)
BIN_FILES := $(SRC_FILES:tests/%=build/%)
BIN_FILES := $(BIN_FILES:%.src=%)
ASM_FILES := $(BIN_FILES:%=%.s)

.PHONY: test
test: $(ASM_FILES) $(BIN_FILES)
	@run_tests

build/%: build/%.s
	as $? -o $@.o
	ld $@.o -o $@

build/%.s: tests/%.src *.py
	mkdir -p build
	./compile.py $< > $@

.PHONY: clean
clean:
	rm build/*
