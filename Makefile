all: help

help:
	# TODO print usage information

install:
	pip install -r requirements.txt

pylint:
	# TODO linting

pytest:
	# TODO testing

docs:
	# TODO docs

run_example_mnist_adjutant:
	PYTHONPATH=. python examples/mnist/mnist_adjutant.py
