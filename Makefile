init:
	@pip install poetry
	@poetry install
	@pre-commit install
	@pre-commit install -t pre-push
	@pre-commit install -t pre-merge-commit

init-stockfish-linux:
	@wget https://stockfish.s3.amazonaws.com/stockfish-11-linux.zip
	@unzip stockfish-11-linux.zip
	@mkdir -p bin
	@cp stockfish-11-linux/Linux/stockfish_20011801_x64_bmi2 bin/stockfish
	@chmod +x bin/stockfish
	@rm -rf stockfish-11-linux
	@rm -rf __MACOSX/
	@rm stockfish-11-linux.zip

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
	@uvicorn chess_blunders.api:app

start-api-dev:
	@uvicorn chess_blunders.api:app --reload

.PHONY: help Makefile docs tests
