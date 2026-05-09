from unittest.mock import MagicMock, patch

import pytest
from freezegun import freeze_time

from app_isitwednesday_reply.handler_reply import lambda_handler
from core.models.social_post import TwitterPostModel, TwitterReplyModel
from core.services.post_service import _build_twitter_reply

IS_WEDNESDAY_SOMEWHERE = "2026-05-05 10:00:00"  # UTC+14 = Wednesday 00:00
NOT_WEDNESDAY_ANYWHERE = "2026-05-04 12:00:00"  # UTC+14 = Tuesday, UTC-12 = Monday


def test_dry_run_skips_twitter():
    result = lambda_handler({"dry_run": True}, None)
    assert result == {"status": "DRY_RUN invoke ok"}


def test_calls_reply_to_recent_wednesday_tweets():
    with patch(
        "app_isitwednesday_reply.handler_reply.app_reply_module"
    ) as mock_module:
        lambda_handler({}, None)
        mock_module.lambda_resource.reply_to_recent_wednesday_tweets.assert_called_once()


@freeze_time(IS_WEDNESDAY_SOMEWHERE)
def test_build_twitter_reply_when_wednesday():
    post = TwitterPostModel(id="1", message="is it wednesday?")
    reply = _build_twitter_reply(post)
    assert reply == TwitterReplyModel(reply_to_id="1", message="Yes, it is Wednesday somewhere.")


@freeze_time(NOT_WEDNESDAY_ANYWHERE)
def test_build_twitter_reply_when_not_wednesday():
    post = TwitterPostModel(id="2", message="is it wednesday?")
    reply = _build_twitter_reply(post)
    assert reply.reply_to_id == "2"
    assert "Wednesday" in reply.message
    assert "Yes" not in reply.message
