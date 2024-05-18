.PHONY: test

export PWD := $(CURDIR)

test:
	PYTHONPATH="$(PWD):$$PYTHONPATH" pytest
