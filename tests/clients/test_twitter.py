from unittest.mock import MagicMock, patch

import pytest

from clients.twitter import TwitterClient


@pytest.fixture
def client():
    return TwitterClient(
        consumer_key="ck",
        consumer_secret="cs",
        bearer_token="bt",
        access_token="at",
        access_token_secret="ats",
    )


def test_bearer_header_returns_authorization(client):
    assert client._bearer_header() == {"Authorization": "Bearer bt"}


def test_bearer_header_raises_when_missing():
    client = TwitterClient(
        consumer_key="x",
        consumer_secret="x",
        bearer_token=None,
        access_token="x",
        access_token_secret="x",
    )
    with pytest.raises(ValueError, match="bearer_token not configured"):
        client._bearer_header()


@patch("clients.twitter.requests.get")
def test_search_recent_tweets_builds_params(mock_get, client):
    mock_get.return_value = MagicMock(
        status_code=200, json=lambda: {"data": [], "meta": {"result_count": 0}}
    )

    client.search_recent_tweets(query="#wed", start_time_iso="2025-01-01T00:00:00Z", since_id="123")

    call = mock_get.call_args
    assert call.kwargs["params"] == {
        "query": "#wed",
        "start_time": "2025-01-01T00:00:00Z",
        "since_id": "123",
    }
    assert call.kwargs["headers"] == {"Authorization": "Bearer bt"}


def test_search_rejects_non_rfc3339_start_time(client):
    with pytest.raises(ValueError, match="RFC3339"):
        client.search_recent_tweets(query="#wed", start_time_iso="2025-01-01T00:00:00")


@patch("clients.twitter.requests.get")
def test_search_raises_on_non_200(mock_get, client):
    mock_get.return_value = MagicMock(status_code=429, text="rate limited")
    with pytest.raises(Exception, match="429"):
        client.search_recent_tweets(query="#wed")


@patch.object(TwitterClient, "_oauth1_session")
def test_post_tweet_builds_payload_with_media_and_reply(mock_session, client):
    mock_post = MagicMock(
        return_value=MagicMock(status_code=201, json=lambda: {"data": {"id": "1"}})
    )
    mock_session.return_value.post = mock_post

    client.post_tweet(text="hi", media_ids=["m1"], reply_tweet_id="42")

    payload = mock_post.call_args.kwargs["json"]
    assert payload == {
        "text": "hi",
        "media": {"media_ids": ["m1"]},
        "reply": {"in_reply_to_tweet_id": "42"},
    }


@patch.object(TwitterClient, "_oauth1_session")
def test_post_tweet_raises_on_non_201(mock_session, client):
    mock_session.return_value.post = MagicMock(return_value=MagicMock(status_code=400, text="bad"))
    with pytest.raises(Exception, match="400"):
        client.post_tweet(text="hi")
