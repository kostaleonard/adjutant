all: help

help:
	@echo "To install required packages, run 'make install' from a clean 'python:3.9' (or higher) conda environment."

install:
	pip install -r requirements.txt

pylint:
	pylint adjutant
	pylint tests

pytest:
	pytest tests --cov=adjutant -m "not slowtest"

pytest_include_slow:
	pytest tests --cov=adjutant

documentation:
	cd docs && make html

package_prod:
	# TODO upload to pypi actual

package_test:
	rm -rf dist
	python3 -m build
	python3 -m twine upload --repository testpypi dist/*

run_example_mnist_adjutant:
	# Examples are run from their own directories, not project root.
	cd examples/mnist && PYTHONPATH=../.. python mnist_adjutant.py

run_example_mnist_model:
	# Examples are run from their own directories, not project root.
	cd examples/mnist && PYTHONPATH=../.. python mnist_model.py
