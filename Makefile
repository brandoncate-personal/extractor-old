# start up virtual environment, make sure vsc interpreter is pointed to correct shell
setup:
	pipenv shell
	pipenv update
	echo "update the python virtual shell with new shell name"

# deploy to google cloud functions using serverless framework
deploy:
	serverless deploy