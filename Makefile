all: help

help:
	# TODO print usage information

install:
	pip install -r requirements.txt

run_example:
	PYTHONPATH=. python adjutant/example.py
