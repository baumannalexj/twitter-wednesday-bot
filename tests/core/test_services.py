from unittest.mock import MagicMock, patch

import pytest

from core import constants
from core.services import WednesdayService


@pytest.fixture
def twitter_mock():
    return MagicMock()


@pytest.fixture
def service(twitter_mock):
    return WednesdayService(twitter_client=twitter_mock)


@patch("core.services.is_wednesday_for_tz", return_value=True)
def test_post_for_today_on_wednesday_includes_media(_, service, twitter_mock):
    service.post_for_today()
    call = twitter_mock.post_tweet.call_args
    assert call.kwargs["text"] in constants.MESSAGES_ITS_WEDNESDAY
    assert call.kwargs["media_ids"] == [constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY]


@patch("core.services.is_wednesday_for_tz", return_value=False)
def test_post_for_today_not_wednesday_no_media(_, service, twitter_mock):
    service.post_for_today()
    call = twitter_mock.post_tweet.call_args
    assert call.kwargs["text"] in constants.MESSAGES_NOT_WEDNESDAY
    assert "media_ids" not in call.kwargs


def test_build_reply_returns_none_when_no_id(service):
    msg, tid = service._build_reply({})
    assert msg is None and tid is None


@patch("core.services.is_it_wednesday_somewhere", return_value=True)
def test_build_reply_when_wednesday_somewhere(_, service):
    msg, tid = service._build_reply({"id": "42"})
    assert msg == "Yes, it is Wednesday somewhere."
    assert tid == "42"


@patch("core.services.is_it_wednesday_somewhere", return_value=False)
@patch("core.services.seconds_until_next_earliest_wednesday", return_value=2 * 24 * 3600 + 3 * 3600)
def test_build_reply_days_message(_secs, _wed, service):
    msg, tid = service._build_reply({"id": "42"})
    assert "2 days" in msg
    assert "3 hours" in msg
    assert tid == "42"


def test_reply_skips_when_no_results(service, twitter_mock):
    twitter_mock.search_recent_tweets.return_value = {"meta": {"result_count": 0}}
    meta = service.reply_to_recent_wednesday_tweets(start_time_iso="2025-01-01T00:00:00Z")
    assert meta == {"result_count": 0}
    twitter_mock.post_tweet.assert_not_called()


@patch("core.services.is_it_wednesday_somewhere", return_value=True)
def test_reply_filters_ineligible_and_replies(_, service, twitter_mock):
    twitter_mock.search_recent_tweets.return_value = {
        "meta": {"result_count": 3},
        "data": [
            {"id": "1", "possibly_sensitive": True, "reply_settings": "everyone"},
            {"id": "2", "possibly_sensitive": False, "reply_settings": "mentionedUsers"},
            {"id": "3", "possibly_sensitive": False, "reply_settings": "everyone"},
        ],
    }
    service.reply_to_recent_wednesday_tweets(start_time_iso="2025-01-01T00:00:00Z")

    posted_replies = [
        c.kwargs.get("reply_tweet_id") for c in twitter_mock.post_tweet.call_args_list
    ]
    assert posted_replies == ["3"]
