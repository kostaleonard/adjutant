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
	# Examples are run from their own directories, not project root.
	cd examples/mnist && PYTHONPATH=../.. python mnist_adjutant.py

run_example_mnist_model:
	# Examples are run from their own directories, not project root.
	cd examples/mnist && PYTHONPATH=../.. python mnist_model.py
