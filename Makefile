.PHONY: check

check:
	@poetry run isort .
	@poetry run black .
	@poetry run flake8 .
	@poetry run bandit -r enterprises
	@poetry run pytest --cov=enterprises --cov-fail-under=90
