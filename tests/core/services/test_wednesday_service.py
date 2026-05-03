import datetime
from unittest.mock import MagicMock, patch

import pytest

from clients.twitter_client import TwitterClient
from core import constants
from core.models.social_post import TwitterPost, TwitterReply
from core.services.wednesday_service import WednesdayService, _build_twitter_reply


@pytest.fixture
def twitter_mock():
    return MagicMock(TwitterClient)


@pytest.fixture
def service(twitter_mock) -> WednesdayService:
    return WednesdayService(client=twitter_mock)


@patch("core.services.wednesday_service.is_it_wednesday_somewhere", return_value=True)
def test_build_reply_when_is_wednesday_somewhere(_, service):
    twitter_reply = _build_twitter_reply(TwitterPost(id="42", message="ssssup"))
    assert twitter_reply.message == "Yes, it is Wednesday somewhere."
    assert twitter_reply.reply_to_id == "42"


@patch("core.services.wednesday_service.is_it_wednesday_somewhere", return_value=True)
def test_post_for_today_posts_with_media_ids_when_its_wednesday(mock_tz, service, twitter_mock):
    service.post_for_today()
    call_args = twitter_mock.post_tweet.call_args
    # call.kwargs is for older python, use call_args.kwargs
    assert call_args.kwargs["text"] in constants.MESSAGES_ITS_WEDNESDAY
    assert call_args.kwargs["media_ids"] == [constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY]


def test_reply_skips_when_no_results(service, twitter_mock):
    twitter_mock.find_recent_hashtags_posts.return_value = []

    # method returns None
    service.reply_to_recent_wednesday_tweets(start_time_iso=datetime.datetime.now(datetime.UTC))

    twitter_mock.reply_to_tweet.assert_not_called()


@patch("core.services.wednesday_service.is_it_wednesday_somewhere", return_value=True)
def test_reply_to_recent_wednesday_tweets_builds_message(mock_somewhere, service, twitter_mock):
    twitter_mock.find_recent_hashtags_posts.return_value = [TwitterPost(id="eligible_1", message="this is message")]

    service.reply_to_recent_wednesday_tweets(datetime.datetime.now(datetime.UTC))

    twitter_mock.reply_to_tweet.assert_called_once_with(
        TwitterReply(reply_to_id="eligible_1", message="Yes, it is Wednesday somewhere.")
    )
