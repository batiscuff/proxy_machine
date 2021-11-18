.PHONY: all lint test test-cov isort black

CMD:=poetry run
PYMODULE:=proxy_machine
TESTS:=tests

style-it: lint black isort
check-it: lint black-check isort-check

lint:
	$(CMD) flake8 $(PYMODULE) $(TESTS)

black:
	$(CMD) black -l 120 $(PYMODULE) $(TESTS)

black-check:
	$(CMD) black -l 120 --check $(PYMODULE) $(TESTS)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

isort:
	$(CMD) isort $(PYMODULE) $(TESTS)

isort-check:
	$(CMD) isort -c $(PYMODULE) $(TESTS)