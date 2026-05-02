
auth:
	aws login

install:
	# --link-mode=copy helps w/ PyCharm syncing (on WSL, my projects are symlinked, the slowdown is negligible but can ignore for macos)
	uv sync --link-mode=copy

# TODO - update packaging to be in app_*/build

package-post-service:
	rm -rf build/lambda/app_isitwednesday_post build/lambda/app_isitwednesday_post.zip
	mkdir -p build/lambda
	uv pip install --target build/lambda/app_isitwednesday_post app-isitwednesday-post
	python -m zipfile -c build/lambda/app_isitwednesday_post.zip build/lambda/app_isitwednesday_post

package-reply-service:
	rm -rf build/lambda/app_isitwednesday_reply build/lambda/app_isitwednesday_reply.zip
	mkdir -p build/lambda
	uv pip install --target build/lambda/app_isitwednesday_reply app-isitwednesday-reply
	python -m zipfile -c build/lambda/app_isitwednesday_reply.zip build/lambda/app_isitwednesday_reply

deploy-post-service: package-post-service
	aws lambda update-function-code \
		--function-name app-isitwednesday-post \
		--zip-file fileb://build/lambda/app_isitwednesday_post.zip \
		--no-cli-pager

deploy-reply-service: package-reply-service
	aws lambda update-function-code \
		--function-name app-isitwednesday-reply \
		--zip-file fileb://build/lambda/app_isitwednesday_reply.zip \
		--no-cli-pager
