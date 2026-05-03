from unittest.mock import patch

from app_isitwednesday_post.handler_post import lambda_handler


def test_dry_run_skips_twitter():
    result = lambda_handler({"dry_run": True}, None)
    assert result == {"status": "dry_run_ok"}


def test_calls_check_if_wednesday_and_post():
    with patch("app_isitwednesday_post.post_service.check_if_wednesday_and_post") as mock_check_if_wednesday_and_post:
        lambda_handler({}, None)
        mock_check_if_wednesday_and_post.assert_called_once()
