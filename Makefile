init:
	@pip install poetry
	@poetry install
	@pre-commit install
	@pre-commit install -t pre-push
	@pre-commit install -t pre-merge-commit

init-stockfish-linux:
	@wget https://stockfishchess.org/files/stockfish_12_linux_x64_bmi2.zip
	@unzip stockfish_12_linux_x64_bmi2.zip
	@mkdir -p bin
	@mv stockfish_20090216_x64_bmi2 bin/stockfish
	@chmod +x bin/stockfish
	@rm stockfish_12_linux_x64_bmi2.zip

init-linux:
	@make init-stockfish-linux
	@make init

tests:
	@python -m pytest --cov=chess_blunders --cov-branch --verbose

integration:
	@pre-commit run --all-files
	@make tests

setuppy:
	@dephell deps convert && black setup.py

deploy-api: ;

start-api-prod:
	@uvicorn chess_blunders.app.api:app

start-api-dev:
	@uvicorn chess_blunders.app.api:app --reload

.PHONY: help Makefile docs tests
