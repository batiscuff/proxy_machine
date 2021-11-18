.PHONY: all lint test test-cov isort black

CMD:=poetry run
PYMODULE:=proxy_machine
TESTS:=tests

style-it: lint black isort

lint:
	$(CMD) flake8 $(PYMODULE) $(TESTS)

black:
	$(CMD) black -l 120 $(PYMODULE) $(TESTS)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

isort:
	$(CMD) isort -c $(PYMODULE) $(TESTS)