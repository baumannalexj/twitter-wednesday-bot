
auth:
	aws login

install:
	uv sync

lint:
	uv run ruff check

test:
	uv run pytest


# --- Post Service (Poster) ---

package-post-service:
	rm -rf build/lambda/post-service build/lambda/package/post-service.zip
	uv pip install --target build/lambda/post-service .
	mkdir -p build/lambda/package
	uv run python -m zipfile -c build/lambda/package/post-service.zip build/lambda/post-service

deploy-post-service: package-post-service
	aws lambda update-function-code \
		--function-name twitter-wednesday-bot-replace-with-autodeploy \
		--zip-file fileb://build/lambda/package/post-service.zip \
		--no-cli-pager

# --- Reply Service (Replier) ---

package-reply-service:
	rm -rf build/lambda/reply-service build/lambda/package/reply-service.zip
	uv pip install --target build/lambda/reply-service .
	mkdir -p build/lambda/package
	uv run python -m zipfile -c build/lambda/package/reply-service.zip build/lambda/reply-service

deploy-reply-service: package-reply-service
	aws lambda update-function-code \
		--function-name reply-to-wednesday-hashtags \
		--zip-file fileb://build/lambda/package/reply-service.zip \
		--no-cli-pager
