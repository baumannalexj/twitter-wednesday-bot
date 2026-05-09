import datetime
import json
import logging

from requests_oauthlib import OAuth1Session

from clients.twitter_response import TweetResponse
from core.models.social_post import TwitterPostModel, TwitterReplyModel
from core.ports.twitter_client_port import ITwitterClient


def _datetime_as_iso_with_zulu_as_string(start_time_iso: datetime.datetime) -> str:
    """
    Twitter api requirement:
        format for as RFC3339 with Z per https://docs.x.com/x-api/posts/search-all-posts#parameter-start-time
    """
    start_time_iso = start_time_iso.astimezone(datetime.UTC).isoformat()  # suffix="+00:00"
    return start_time_iso.replace("+00:00", "Z")


def _filter_out_ineligible_tweets(response_json) -> list[TwitterPostModel]:
    tweets_data = response_json.get("data", [])

    tweets: list[TweetResponse] = [TweetResponse(**tweet) for tweet in tweets_data]

    eligible_tweets = [TwitterPostModel(id=tweet.id, message=tweet.text) for tweet in tweets if tweet.is_eligible()]
    return eligible_tweets


class TwitterClient(ITwitterClient):
    URL_TWEET = "https://api.twitter.com/2/tweets"
    URL_SEARCH = "https://api.twitter.com/2/tweets/search/recent"

    _client: OAuth1Session

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str):

        if not consumer_key:
            raise ValueError("consumer_key must be provided")
        if not consumer_secret:
            raise ValueError("consumer_secret must be provided")
        if not access_token:
            raise ValueError("access_token must be provided")
        if not access_token_secret:
            raise ValueError("access_token_secret must be provided")

        self._client = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

    def find_recent_hashtags_posts(
        self,
        hashtags_to_search: list[str],
        start_time_iso: datetime.datetime,
        since_id: str | None = None,
        max_results: int | None = None,
    ) -> list[TwitterPostModel]:

        query = " OR ".join(hashtags_to_search)
        params: dict = {"query": query}

        if start_time_iso:
            # Accept datetime or ISO string; normalize to RFC3339 with Z suffix
            if start_time_iso.tzinfo is None:
                raise ValueError(f"start_time datetime must be timezone-aware: {start_time_iso}")

            start_time_utc = _datetime_as_iso_with_zulu_as_string(start_time_iso)
            params["start_time"] = start_time_utc
        if since_id:
            params["since_id"] = since_id
        if max_results:
            params["max_results"] = max_results

        response = self._client.get(self.URL_SEARCH, params=params)
        if response.status_code != 200:
            logging.error(f"Twitter search failed: {response.status_code=} {response.text=}")
            raise Exception(f"Twitter search failed: {response.status_code}")

        response_json = response.json()

        meta = response_json.get("meta", {})
        result_count = meta.get("result_count", 0)

        if not result_count:
            logging.info(f"No tweets found: {hashtags_to_search=}, {meta=}")
            return []

        if response_json.get("next_token"):
            logging.warning(f"next_token present but pagination not implemented. {meta=}")

        eligible_tweets = _filter_out_ineligible_tweets(response_json)
        if not eligible_tweets:
            all_tweets: list[TweetResponse] = [TweetResponse(**t) for t in response_json.get("data", [])]
            ineligible = [{"post_id": t.id, "reply_setting": t.reply_settings} for t in all_tweets]
            logging.warning(f"No eligible tweets found out of {result_count=}: {ineligible}")

        return eligible_tweets

    def post_tweet(self, message_string: str, media_ids: list[str] | None = None) -> TwitterPostModel:

        payload: dict = {"text": message_string}
        if media_ids:
            payload["media"] = {"media_ids": media_ids}

        response = self._client.post(self.URL_TWEET, json=payload)
        if response.status_code != 201:
            logging.error(f"Twitter post failed: {response.status_code=} {response.text=}")
            raise Exception(f"Twitter post failed: {response.status_code}")

        body = response.json()
        logging.info(f"Tweet posted: {json.dumps(body, indent=4)}")
        tweet_response = TweetResponse(**body.get("data"))
        return TwitterPostModel(tweet_response.id, tweet_response.text)

    def reply_to_tweet(self, post_reply: TwitterReplyModel) -> TwitterPostModel:

        payload: dict = {"text": post_reply.message, "reply": {"in_reply_to_tweet_id": post_reply.reply_to_id}}

        response = self._client.post(self.URL_TWEET, json=payload)
        if response.status_code != 201:
            logging.error(
                f"Twitter reply failed for {post_reply.reply_to_id=}: {response.status_code=} {response.text=}."
            )
            raise Exception(f"Twitter reply failed: {response.status_code}")

        body = response.json()
        logging.info(f"Tweet reply posted: {json.dumps(body, indent=4)}")
        tweet_response = TweetResponse(**body.get("data"))
        return TwitterPostModel(tweet_response.id, tweet_response.text)
