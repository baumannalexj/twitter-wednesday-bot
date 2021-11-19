
# run $poetry shell prior to making
build:
	echo 'hi'
	poetry env use python3.9
	poetry install
	poetry env info --path

package:
	poetry build
	rm -rf dist/artifact.zip
	poetry run pip install --upgrade --target dist/package dist/*.whl
	cd dist/package && zip -r ../artifact.zip . -x '*.pyc'

deploy-post-service:
	aws lambda update-function-code\
 	--function-name twitter-wednesday-bot-replace-with-autodeploy\
 	--zip-file fileb://dist/artifact.zip\

# how to set handler and runtime here?


deploy-reply-service:
	aws lambda update-function-code\
 	--function-name reply-to-wednesday-hashtags\
 	--zip-file fileb://dist/artifact.zip
	#--handler src/listening/lambda_listening.handler how to set handler and runtime here?



