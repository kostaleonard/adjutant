all: help

help:
	# TODO print usage information

install:
	pip install -r requirements.txt

run_example_mnist_adjutant:
	PYTHONPATH=. python examples/mnist/mnist_adjutant.py
