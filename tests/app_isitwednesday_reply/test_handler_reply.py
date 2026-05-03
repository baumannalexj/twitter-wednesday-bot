from unittest.mock import patch

from app_isitwednesday_reply.handler_reply import lambda_handler


def test_dry_run_skips_twitter():
    result = lambda_handler({"dry_run": True}, None)
    assert result == {"status": "DRY_RUN invoke ok"}


def test_calls_reply_to_recent_wednesday_tweets():
    with patch(
        "app_isitwednesday_reply.handler_reply.post_service.reply_to_recent_wednesday_tweets"
    ) as mock_reply_to_recent_wednesday_tweets:
        lambda_handler({}, None)
        mock_reply_to_recent_wednesday_tweets.assert_called_once()
