import datetime
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from core import constants
from core.date_helper import EARLIEST_TZ, LATEST_TZ
from core.models.social_post import TwitterPostModel, TwitterReplyModel
from core.ports.twitter_client_port import ITwitterClient
from core.services.post_service import PostService

WEDNESDAY_MIDNIGHT_UTC = datetime.datetime.fromisoformat("2026-05-06T00:00:00Z")  # TZ aware
EARLIEST_WEDNESDAY_MIDNIGHT = datetime.datetime.fromisoformat("2026-05-06T00:00:00").replace(tzinfo=EARLIEST_TZ)
LATEST_WEDNESDAY_MIDNIGHT = datetime.datetime.fromisoformat("2026-05-06T00:00:00").replace(tzinfo=LATEST_TZ)


class MockTwitterClient(MagicMock(ITwitterClient)):
    """surfaces interface for typeahead"""


mock_twitter_client = MockTwitterClient()
post_service = PostService(_client=mock_twitter_client)


@pytest.fixture(autouse=True)
def reset_mocks():
    mock_twitter_client.reset_mock()
    yield  # reset before, not after


@freeze_time(EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(hours=2))
def test_when_not_wednesday_then_check_if_wednesday_posts_non_wednesday_post():
    post_service.check_if_wednesday_and_post()
    call_args = mock_twitter_client.post_tweet.call_args
    assert call_args.kwargs["message_string"] in constants.MESSAGES_NOT_WEDNESDAY
    assert "media_ids" not in call_args.kwargs


@freeze_time(WEDNESDAY_MIDNIGHT_UTC)
def test_when_is_wednesday_then_check_if_wednesday_posts_wednesday_post():
    post_service.check_if_wednesday_and_post()
    call_args = mock_twitter_client.post_tweet.call_args
    assert call_args.kwargs["message_string"] in constants.MESSAGES_ITS_WEDNESDAY
    assert call_args.kwargs["media_ids"] == [constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY]


@freeze_time(WEDNESDAY_MIDNIGHT_UTC)
def test_when_twitter_client_throws_exception_then_exception_is_raised():
    mock_twitter_client.post_tweet.side_effect = RuntimeError("Twitter API error")
    with pytest.raises(RuntimeError, match="Twitter API error"):
        post_service.check_if_wednesday_and_post()


@pytest.mark.parametrize(
    "start_time_iso,expected_message",
    [
        (
            LATEST_WEDNESDAY_MIDNIGHT + datetime.timedelta(days=1),
            "Still 4 days and 22 hours until Earth sees Wednesday.",
        ),
        (
            EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(days=1, hours=2),
            "Still 1 day and 2 hours until Earth sees Wednesday.",
        ),
        (
            EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(hours=2, minutes=1),
            "We're 2 hours and 1 minutes away until Earth hits Wednesday.",
        ),
        (
            EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(minutes=1, seconds=59),
            "Earth is just 1 minute and 59 seconds from Wednesday.",
        ),
        (
            EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(seconds=1),
            "Buckle up! 1 second until Earth enters Wednesday.",
        ),
    ],
)
@freeze_time(WEDNESDAY_MIDNIGHT_UTC)
def test_build_twitter_reply_not_wednesday_message_format(start_time_iso: datetime.datetime, expected_message):
    """Tests if the date calculation and message work,
    compares the earliest wednesday TZ and the latest wednesday TZ to see if it's wednesday somewhere on earth
    """
    with freeze_time(start_time_iso):
        mock_post = TwitterPostModel(id="1", message="#isitwednesdayyet")
        expected_twitter_reply_model = TwitterReplyModel(reply_to_id="1", message=expected_message)

        mock_twitter_client.find_recent_hashtags_posts.return_value = [mock_post]

        post_service.reply_to_recent_wednesday_tweets(start_time_iso)

        assert (
            mock_twitter_client.find_recent_hashtags_posts.call_args.kwargs["hashtags_to_search"]
            == constants.SEARCH_TERMS_WEDNESDAY_HASHTAGS
        )

        assert mock_twitter_client.find_recent_hashtags_posts.call_args.kwargs["start_time_iso"] == start_time_iso
        mock_twitter_client.reply_to_tweet.assert_called_once_with(expected_twitter_reply_model)


@freeze_time(WEDNESDAY_MIDNIGHT_UTC)
def test_when_is_wednesday_then_reply_to_recent_wednesday_tweets_replies_with_wednesday_message():
    mock_twitter_client.find_recent_hashtags_posts.return_value = [TwitterPostModel(id="2", message="is it wednesday?")]
    post_service.reply_to_recent_wednesday_tweets(start_time_iso=datetime.datetime.now(datetime.UTC))
    mock_twitter_client.reply_to_tweet.assert_called_once_with(
        TwitterReplyModel(reply_to_id="2", message="Yes, it is Wednesday somewhere.")
    )
