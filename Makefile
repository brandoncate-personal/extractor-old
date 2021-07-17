# start up virtual environment, make sure vsc interpreter is pointed to correct shell
setup:
	pipenv shell

# deploy to google cloud functions using serverless framework
deploy:
	serverless deploy