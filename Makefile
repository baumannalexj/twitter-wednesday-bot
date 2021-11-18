

build:
	echo 'hi'
	poetry env use python3.9
	poetry install
	poetry env info --path

package:
	poetry build
	rm -rf dist/artifact.zip
	poetry run pip install --upgrade -t dist/package dist/*.whl
	cd dist/package && zip -r ../artifact.zip . -x '*.pyc'

deploy:
	aws lambda update-function-code\
 	--function-name twitter-wednesday-bot-replace-with-autodeploy\
 	--zip-file fileb://dist/artifact.zip




