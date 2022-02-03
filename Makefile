.PHONY: all lint test type publish docs
CMD:=poetry run

lint:
	$(CMD) black .

type:
	$(CMD) mypy . --exclude=build/

test:
	$(CMD) pytest

build: # build for release
	python setup.py sdist bdist_wheel

publish:
	$(CMD) publish

docs:
	sphinx-build docs/source docs/build