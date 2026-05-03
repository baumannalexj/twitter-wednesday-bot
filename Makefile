
auth:
	aws login

install:
	uv sync

lint:
	uv run ruff check

test:
	uv run pytest


# --- Post Service (Poster) ---

package-service-post:
	rm -rf build/lambda/post-service build/lambda/package/post-service.zip
	uv pip install --target build/lambda/post-service .
	mkdir -p build/lambda/package
	uv run python -m zipfile -c build/lambda/package/post-service.zip build/lambda/post-service

deploy-service-post: package-service-post
	aws lambda update-function-code \
		--function-name twitter-wednesday-bot-replace-with-autodeploy \
		--zip-file fileb://build/lambda/package/post-service.zip \
		--no-cli-pager

# --- Reply Service (Replier) ---

package-service-reply:
	rm -rf build/lambda/reply-service build/lambda/package/reply-service.zip
	uv pip install --target build/lambda/reply-service .
	mkdir -p build/lambda/package
	uv run python -m zipfile -c build/lambda/package/reply-service.zip build/lambda/reply-service

deploy-service-reply: package-service-reply
	aws lambda update-function-code \
		--function-name reply-to-wednesday-hashtags \
		--zip-file fileb://build/lambda/package/reply-service.zip \
		--no-cli-pager
