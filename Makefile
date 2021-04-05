POETRY := poetry run

lint:
	$(POETRY) pylint vim_clutchify
	$(POETRY) mypy vim_clutchify
