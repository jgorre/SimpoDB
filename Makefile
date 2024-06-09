.PHONY: test

export PWD := $(CURDIR)

test:
	PYTHONPATH="$(PWD):$$PYTHONPATH" pytest $(args)

run:
	python3 main.py