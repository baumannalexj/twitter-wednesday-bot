from unittest.mock import patch, MagicMock

import pytest
from app_isitwednesday_post import AppModule, AppConfiguration, LambdaResource
from app_isitwednesday_post.handler_post import lambda_handler
from core import PostService

config = AppConfiguration(
    "test_consumer_key",
    "test_consumer_secret",
    "test_access_token",
    "test_access_token_secret",
)


mock_post_service= MagicMock(spec=PostService)

lambda_resource = LambdaResource(post_service=mock_post_service)

app_post_module = AppModule(config)

# app_post_module.lambda_resource = lambda_resource


@pytest.fixture(autouse=True)
def app_module(mock_post_service):
    app_post_module = AppModule(config)

    lambda_resource = LambdaResource(post_service=mock_post_service),

    with patch("app_isitwednesday_post.handler_post.app_post_module", app_post_module):
        yield app_post_module


@pytest.fixture
def mock_post_service():
    return MagicMock(spec=PostService)


def test_dry_run_skips_twitter():
    result = lambda_handler({"dry_run": True}, None)
    assert result == {"status": "dry_run_ok"}


def test_calls_check_if_wednesday_and_post():
    with patch("app_isitwednesday_post.post_service.check_if_wednesday_and_post") as mock_check_if_wednesday_and_post:
        lambda_handler({}, None)
        mock_check_if_wednesday_and_post.assert_called_once()
