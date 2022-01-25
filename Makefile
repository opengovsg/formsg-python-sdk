.PHONY: all lint test type publish
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