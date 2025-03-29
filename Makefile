VENV := PYTHONPATH="." poetry run

lint: mypy black ruff
lint-fix: black ruff-fix

mypy:
	$(VENV) mypy crypkit tests

black:
	$(VENV) black crypkit tests

ruff:
	$(VENV) ruff check crypkit tests

ruff-fix:
	$(VENV) ruff check --fix crypkit tests
