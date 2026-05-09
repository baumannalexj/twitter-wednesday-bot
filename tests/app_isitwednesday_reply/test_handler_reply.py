import datetime
from unittest.mock import MagicMock, patch

import pytest
from freezegun import freeze_time

from app_config.config import config
from app_isitwednesday_reply import AppModule
from app_isitwednesday_reply.handler_reply import lambda_handler
from core.services.post_service import PostService

IS_WEDNESDAY_SOMEWHERE = datetime.datetime.fromisoformat("2026-05-05T10:00:00Z")  # UTC+14 = Wednesday 00:00
NOT_WEDNESDAY_ANYWHERE = datetime.datetime.fromisoformat("2026-05-04T12:00:00Z")  # UTC+14 = Tuesday, UTC-12 = Monday


class MockPostService(MagicMock(PostService)):
    """surfaces interface for typeahead"""


mock_post_service = MockPostService()
app_reply_module = AppModule(post_service=mock_post_service)


@pytest.fixture(autouse=True)
def reset_mocks():
    mock_post_service.reset_mock()
    with patch("app_isitwednesday_reply.handler_reply.app_reply_module", app_reply_module):
        yield


def test_dry_run_skips_twitter():
    result = lambda_handler({"dry_run": True}, None)
    assert result == {"status": "DRY_RUN invoke ok"}


@freeze_time(IS_WEDNESDAY_SOMEWHERE)
def test_calls_reply_to_recent_wednesday_tweets():
    lambda_handler({}, None)
    mock_post_service.reply_to_recent_wednesday_tweets.assert_called_with(
        start_time_iso=IS_WEDNESDAY_SOMEWHERE - datetime.timedelta(minutes=config.reply_cron_interval_minutes)
    )
