all: help

help:
	# TODO print usage information

install:
	pip install -r requirements.txt

run_example:
	#cd src && PYTHONPATH=$(PYTHONPATH):.. python example.py
	PYTHONPATH=. python src/example.py
