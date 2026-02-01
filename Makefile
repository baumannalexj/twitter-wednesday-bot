
build:
	python3.9 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"

package-cron:
	rm -rf dist/cron-package dist/cron-artifact.zip
	.venv/bin/pip install --upgrade --target dist/cron-package ./core ./clients ./app_lambda_handler_isitwednesday_cron
	cd dist/cron-package && zip -r ../cron-artifact.zip . -x '*.pyc'

package-listener:
	rm -rf dist/listener-package dist/listener-artifact.zip
	.venv/bin/pip install --upgrade --target dist/listener-package ./core ./clients ./app_lambda_handler_social_listener
	cd dist/listener-package && zip -r ../listener-artifact.zip . -x '*.pyc'

deploy-post-service: package-cron
	aws lambda update-function-code \
		--function-name twitter-wednesday-bot-replace-with-autodeploy \
		--zip-file fileb://dist/cron-artifact.zip
	aws lambda update-function-configuration \
		--function-name twitter-wednesday-bot-replace-with-autodeploy \
		--handler app_lambda_handler_isitwednesday_cron.lambda_handler.lambda_handler

deploy-reply-service: package-listener
	aws lambda update-function-code \
		--function-name reply-to-wednesday-hashtags \
		--zip-file fileb://dist/listener-artifact.zip
	aws lambda update-function-configuration \
		--function-name reply-to-wednesday-hashtags \
		--handler app_lambda_handler_social_listener.lambda_handler.handler
