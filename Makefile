.PHONY: test

export PWD := $(CURDIR)

test:
	PYTHONPATH="$(PWD):$$PYTHONPATH" pytest

run:
	python3 main.py