
auth:
	aws login

install:
	uv sync

lint:
	uv run ruff check

test:
	uv run pytest

HANDLER_LOCATION_POST=app_isitwednesday_post.handler_post.lambda_handler
HANDLER_LOCATION_REPLY=app_isitwednesday_reply.handler_reply.lambda_handler
LAMBDA_FUNCTION_NAME_ISITWEDNESDAY_POST=twitter-wednesday-bot-replace-with-autodeploy
LAMBDA_FUNCTION_NAME_ISITWEDNESDAY_REPLY=reply-to-wednesday-hashtags
TARGET_LAMBDA_FUNCTION_NAME= # set when calling make package: make package TARGET_FUNCTION_NAME=twitter-wednesday-bot-replace-with-autodeploy
TARGET_LAMBDA_HANDLER_LOCATION=


package:
	# REQUIRES PARAMETER: make package TARGET_FUNCTION_NAME=twitter-wednesday-bot-replace-with-autodeploy
	# Same package for both, the lambda handler function-name is updated during deploy
	echo "packaging $(TARGET_LAMBDA_FUNCTION_NAME) for lambda"
	echo ""

	rm -rf build/lambda
	rm -rf build/package
	mkdir -p build/lambda build/package
	uv pip install --target build/lambda .
	cd build/lambda && zip -qr $(CURDIR)/build/package/$(TARGET_LAMBDA_FUNCTION_NAME).zip . \
		-x '*.pyc' \
		-x '*/__pycache__/*' \
		-x '*.dist-info/*' \
		-x 'bin/*'

_deploy_helper:
	echo "deploying: $(TARGET_LAMBDA_FUNCTION_NAME)"
	echo ""
	aws lambda update-function-code \
		--function-name $(TARGET_LAMBDA_FUNCTION_NAME) \
		--zip-file fileb://build/package/$(TARGET_LAMBDA_FUNCTION_NAME).zip \
		--no-cli-pager

	echo "waiting for deploy $(TARGET_LAMBDA_FUNCTION_NAME)..."
	echo ""
	aws lambda wait function-updated \
 		--function-name $(TARGET_LAMBDA_FUNCTION_NAME) \
 		--no-cli-pager

	echo "updating lambda handler path to: $(TARGET_LAMBDA_HANDLER_LOCATION)"
	echo ""
	aws lambda update-function-configuration \
      --function-name $(TARGET_LAMBDA_FUNCTION_NAME) \
      --handler $(TARGET_LAMBDA_HANDLER_LOCATION) \
      --no-cli-pager

	$(MAKE) smoke-post


deploy-service-post: TARGET_LAMBDA_FUNCTION_NAME=$(LAMBDA_FUNCTION_NAME_ISITWEDNESDAY_POST)
deploy-service-post: TARGET_LAMBDA_HANDLER_LOCATION=$(HANDLER_LOCATION_POST)
deploy-service-post: package _deploy_helper
	echo "packaging and deploying function:$(TARGET_LAMBDA_FUNCTION_NAME), handler: $(TARGET_LAMBDA_HANDLER_LOCATION)"

deploy-service-reply: TARGET_LAMBDA_FUNCTION_NAME=$(LAMBDA_FUNCTION_NAME_ISITWEDNESDAY_REPLY)
deploy-service-reply: TARGET_LAMBDA_HANDLER_LOCATION=$(HANDLER_LOCATION_REPLY)
deploy-service-reply: package _deploy_helper
	echo "packaging and deploying function:$(TARGET_LAMBDA_FUNCTION_NAME), handler: $(TARGET_LAMBDA_HANDLER_LOCATION)"


smoke-post:
	echo "smoke testing post lambda..."
	echo ""
	aws lambda invoke \
		--function-name $(LAMBDA_FUNCTION_NAME_ISITWEDNESDAY_POST) \
		--payload '{"dry_run": true}' \
		--cli-binary-format raw-in-base64-out \
		/dev/stdout \
		--no-cli-pager

smoke-reply:
	echo "smoke testing reply lambda..."
	echo ""
	aws lambda invoke \
		--function-name $(LAMBDA_FUNCTION_NAME_ISITWEDNESDAY_REPLY) \
		--payload '{"dry_run": true}' \
		--cli-binary-format raw-in-base64-out \
		/dev/stdout \
		--no-cli-pager
