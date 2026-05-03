
auth:
	aws login

test:
	uv run pytest

install:
	uv sync --link-mode=copy

package-post-service:
	rm -rf build/lambda/twitter-wednesday-bot build/lambda/package/twitter-wednesday-bot.zip
	uv pip install --target build/lambda/twitter-wednesday-bot .
	mkdir -p build/lambda/package
	python -m zipfile -c build/lambda/package/twitter-wednesday-bot.zip build/lambda/twitter-wednesday-bot

package-reply-service:
	rm -rf build/lambda/reply-to-wednesday-hashtags build/lambda/package/reply-to-wednesday-hashtags.zip
	uv pip install --target build/lambda/reply-to-wednesday-hashtags .
	mkdir -p build/lambda/package
	python -m zipfile -c build/lambda/package/reply-to-wednesday-hashtags.zip build/lambda/reply-to-wednesday-hashtags

deploy-post-service: package-post-service
	aws lambda update-function-code \
		--function-name twitter-wednesday-bot-replace-with-autodeploy \
		--zip-file fileb://build/lambda/package/twitter-wednesday-bot.zip \
		--no-cli-pager

deploy-reply-service: package-reply-service
	aws lambda update-function-code \
		--function-name reply-to-wednesday-hashtags \
		--zip-file fileb://build/lambda/package/reply-to-wednesday-hashtags.zip \
		--no-cli-pager
