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
	@npm install -g serverless
	@npm install serverless-python-requirements
	@npm install netlify-cli -g

init-stockfish-linux:
	@wget https://stockfishchess.org/files/stockfish_12_linux_x64_bmi2.zip
	@unzip stockfish_12_linux_x64_bmi2.zip
	@mkdir -p bin
	@mv stockfish_20090216_x64_bmi2 bin/stockfish
	@chmod +x bin/stockfish
	@rm stockfish_12_linux_x64_bmi2.zip

init-stockfish-macosx: ;

init-linux:
	@$(MAKE) init-stockfish-linux
	@$(MAKE) init

init-macosx:
	@$(MAKE) init-stockfish-macosx
	@$(MAKE) init


# ------------------------------------------------------------------------------------ #
#                                     Dependencies                                     #
#																																											 #
#                                     deps api pip                                     #
# ------------------------------------------------------------------------------------ #
deps-api-pip:
	@dephell deps convert --envs main --to-format=pip --to-path=chess_blunders/app/api/requirements.txt
	@echo '../../../' >> chess_blunders/app/api/requirements.txt


# ------------------------------------------------------------------------------------ #
#                                         CI/CD                                        #
#																																											 #
#                                         tests                                        #
#                                    deploy-api-prod                                   #
#                                    deploy-api-dev                                    #
#                                       build-web                                      #
#                                    deploy-web-prod                                   #
#                                    deploy-web-dev                                    #
#                                       ci-tests                                       #
#                                    ci-integration                                    #
#                                     ci-deployment                                    #
# ------------------------------------------------------------------------------------ #
tests:
	@python -m pytest --cov=chess_blunders --cov-branch --verbose

deploy-api-prod:
	@cd chess_blunders/app/api && sls deploy --stage prod

deploy-api-dev:
	@cd chess_blunders/app/api && sls deploy --stage dev

build-web:
	@npm --prefix chess_blunders/app/web run build

deploy-web-prod:
	@$(MAKE) build-web
	@netlify deploy --prod

deploy-web-dev:
	@$(MAKE) build-web
	@netlify deploy

ci-tests:
	@$(MAKE) tests

ci-integration:
	@pre-commit run --all-files
	@$(MAKE) ci-tests

ci-deployment: ;
