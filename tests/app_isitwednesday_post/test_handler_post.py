from unittest.mock import MagicMock, patch

import pytest

from app_isitwednesday_post import AppModule
from app_isitwednesday_post.handler_post import lambda_handler  # noqa: F401 — smoke test: fails if packaging is broken
from app_isitwednesday_post.handler_post import lambda_handler
from core.services.post_service import PostService


class MockPostService(MagicMock(PostService)):
    """surfaces interface for typeahead"""


mock_post_service = MockPostService()
app_post_module = AppModule(post_service=mock_post_service)


@pytest.fixture(autouse=True)
def reset_mocks():
    mock_post_service.reset_mock()
    with patch("app_isitwednesday_post.handler_post.app_post_module", app_post_module):
        yield


def test_dry_run_skips_twitter():
    result = lambda_handler({"dry_run": True}, None)
    assert result == {"status": "dry_run_ok"}


def test_calls_check_if_wednesday_and_post():
    lambda_handler({}, None)
    mock_post_service.check_if_wednesday_and_post.assert_called_once()
