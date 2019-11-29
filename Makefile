black-check:
	black --check --diff --exclude migrations .

black-lint:
	black --exclude migrations .

unit-tests:
	coverage run -m unittest
	coverage report

integration-tests:
	pytest -m "db_operations"
