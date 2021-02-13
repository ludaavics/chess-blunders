.PHONY: help Makefile docs tests

# ------------------------------------------------------------------------------------ #
#                                    Initialization                                    #
#																																										   #
#                                         init                                         #
#                                 init-stockfish-linux                                 #
#                                 init-stockfish-macosx                                #
#                                    init-serverless                                   #
#                                      init-linux                                      #
#                                      init-macosx                                     #
# ------------------------------------------------------------------------------------ #
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

init-stockfish-macosx: ;

init-serverless:
	@npm install -g serverless
	@npm install serverless-python-requirements

init-linux:
	@make init
	@make init-stockfish-linux
	@make init-serverless

init-macosx:
	@make init
	@make init-stockfish-macosx
	@make init-serverless


# ------------------------------------------------------------------------------------ #
#                                     Dependencies                                     #
#																																											 #
#                                     deps setup-py                                    #
#                                     deps api pip                                     #
# ------------------------------------------------------------------------------------ #
deps-setup-py:
	@dephell deps convert && black setup.py

deps-api-pip:
	@dephell deps convert --to-format=pip --to-path=chess_blunders/app/api/requirements.txt
	@echo '../../../' >> chess_blunders/app/api/requirements.txt


# ------------------------------------------------------------------------------------ #
#                                         CI/CD                                        #
#																																											 #
#                                         tests                                        #
#                                       ci-tests                                       #
#                                    ci-integration                                    #
#                                     ci-deployment                                    #
# ------------------------------------------------------------------------------------ #
tests:
	@python -m pytest --cov=chess_blunders --cov-branch --verbose

ci-tests:
	@make tests

ci-integration:
	@pre-commit run --all-files
	@make ci-cd-tests

ci-deployment: ;

# ------------------------------------------------------------------------------------ #
#                                      API Server                                      #
#																																											 #
#                                    start-api-prod                                    #
#                                     start-api-dev                                    #
# ------------------------------------------------------------------------------------ #
start-api-prod:
	@uvicorn chess_blunders.app.api.main:app

start-api-dev:
	@uvicorn chess_blunders.app.api.main:app --reload
