init:
	@pip install poetry
	@poetry install
	@pre-commit install
	@pre-commit install -t pre-push
	@pre-commit install -t pre-merge-commit

tests:
	@python -m pytest --cov=chess_blunders --cov-branch --verbose

integration:
	@pre-commit run --all-files
	@make tests

setuppy:
	@dephell deps convert && black setup.py

deploy-api: ;

start-api-prod:
	@uvicorn chess_blunders.api:app

start-api-dev:
	@uvicorn chess_blunders.api:app --reload

.PHONY: help Makefile docs tests
