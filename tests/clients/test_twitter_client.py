import datetime
import json
import os
from unittest.mock import MagicMock, patch

import freezegun
import pytest
from tests.clients.responses.twitter_api_json import response_twitter_search, response_post_tweet, response_post_reply
from clients.twitter_client import TwitterClient  # Replace with your actual module name
from core.date_helper import get_time_min_ago
from core.models.social_post import TwitterPostModel, TwitterReplyModel


def load_response(filename: str):
    """Helper to load saved JSON responses"""
    path = os.path.join("tests", "clients", "responses", filename)
    with open(path) as f:
        return json.load(f)


class TestTwitterClient:
    @pytest.fixture
    def mock_session(self):
        with patch("clients.twitter_client.OAuth1Session") as mock:
            yield mock.return_value

    @pytest.fixture
    def client(self, mock_session):
        return TwitterClient(
            consumer_key="test", consumer_secret="test", access_token="test", access_token_secret="test"
        )

    ## --- Tests for find_recent_hashtags_posts ---

    def test_find_recent_hashtags_posts_from_json(self, client, mock_session):
        """find_recent_hashtags_posts should filter out non eligible tweets"""
        json_data = response_twitter_search

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = json_data
        mock_session.get.return_value = mock_response

        start_time = datetime.datetime.now(datetime.UTC)
        posts: list[TwitterPostModel] = client.find_recent_hashtags_posts(
            hashtags_to_search=["#notarealhashtag"], start_time_iso=start_time
        )

        # In response_post_search.json we had 2 eligible tweets
        assert len(posts) == 2
        assert posts[0].id == "1461374568799604741"
        assert posts[0].message == "#isitwednesday eligible with reply_settings=everyone"
        assert posts[1].id == "1461374568799604742"
        assert posts[1].message == "#isitwednesday this is eligible without the reply_settings"

    ## --- Tests for post_tweet ---

    def test_post_tweet_from_json(self, client, mock_session):
        json_data = response_post_tweet

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = json_data
        mock_session.post.return_value = mock_response

        result: TwitterPostModel = client.post_tweet(message_string="Hello world!", media_ids=[])

        # Verify the returned ID matches our JSON file
        assert result.id == "1445827346513514498"

        # Verify the outgoing payload was constructed correctly
        sent_json = mock_session.post.call_args[1]["json"]
        assert sent_json["text"] == "Hello world!"

    ## --- Tests for reply_to_tweet ---

    def test_reply_to_tweet_from_json(self, client, mock_session):
        json_data = response_post_reply

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = json_data
        mock_session.post.return_value = mock_response

        target_id = "111222"
        result: TwitterPostModel = client.reply_to_tweet(
            post_reply=TwitterReplyModel(target_id, message="it's not wednesday yet")
        )

        # Verify the outgoing request maps to the X API reply structure
        sent_json = mock_session.post.call_args[1]["json"]
        assert sent_json["reply"]["in_reply_to_tweet_id"] == target_id
        assert result.id == "1445827346513514500"

    ## --- Logic & Utility Tests ---

    @freezegun.freeze_time("2021-12-25T10:30:00")
    def test_datetime_to_zulu_conversion(self, client, mock_session):
        """Tests the _datetime_as_iso_with_zulu_as_string logic via the client"""
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"meta": {"result_count": 0}}
        mock_session.get.return_value = mock_response

        test_dt = get_time_min_ago(10)  # same method that lambda_handler injects: "2021-12-25T10:20:00"
        client.find_recent_hashtags_posts(hashtags_to_search=["#testhashtag"], start_time_iso=test_dt)

        params = mock_session.get.call_args[1]["params"]
        # Ensure the +00:00 is replaced by Z as per X API requirements
        assert params["start_time"] == "2021-12-25T10:20:00Z"

    def test_api_failure_handling(self, client, mock_session):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"errors": [{"message": "Invalid Request"}]}'
        mock_session.get.return_value = mock_response

        with pytest.raises(Exception) as excinfo:
            client.find_recent_hashtags_posts(
                hashtags_to_search=["#fail"], start_time_iso=datetime.datetime.now(datetime.UTC)
            )

        assert "Twitter search failed: 400" in str(excinfo.value)
