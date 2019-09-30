.PHONY: clean-pyc clean-build docs

clean: clean-build clean-pyc

test:
	pipenv run pytest tests
