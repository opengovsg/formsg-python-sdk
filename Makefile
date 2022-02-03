.PHONY: all lint test type publish docs build
CMD:=poetry run

lint:
	$(CMD) black .

type:
	$(CMD) mypy . --exclude=build/ --exclude=example_app

test:
	python -m pytest tests

build: # build for release
	python setup.py sdist bdist_wheel

publish:
	$(CMD) publish

docs:
	sphinx-build docs/source docs/build