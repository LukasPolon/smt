all: black-check unit-tests integration-tests

black-check:
	black --check --diff app/
	black --check --diff tests/

black-lint:
	black app/
	black tests/

unit-tests:
	coverage run -m unittest

integration-tests:
	pytest -m "db_operations"
