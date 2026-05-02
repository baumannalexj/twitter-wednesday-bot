import json
import logging

import requests
from requests_oauthlib import OAuth1Session


class TwitterClient:
    URL_TWEET = "https://api.twitter.com/2/tweets"
    URL_SEARCH = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        bearer_token: str,
        access_token: str,
        access_token_secret: str,
    ):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._bearer_token = bearer_token
        self._access_token = access_token
        self._access_token_secret = access_token_secret

    def _bearer_header(self) -> dict:
        if not self._bearer_token:
            raise ValueError("TwitterClient: bearer_token not configured")
        return {"Authorization": f"Bearer {self._bearer_token}"}

    def _oauth1_session(self) -> OAuth1Session:
        return OAuth1Session(
            client_key=self._consumer_key,
            client_secret=self._consumer_secret,
            resource_owner_key=self._access_token,
            resource_owner_secret=self._access_token_secret,
        )

    def search_recent_tweets(
        self,
        query: str,
        start_time_iso: str | None = None,
        since_id: str | None = None,
        max_results: int | None = None,
    ) -> dict:
        params: dict = {"query": query}
        if start_time_iso:
            if not str(start_time_iso).endswith("Z"):
                raise ValueError(f"start_time must be RFC3339+Z: {start_time_iso}")
            params["start_time"] = start_time_iso
        if since_id:
            params["since_id"] = since_id
        if max_results:
            params["max_results"] = max_results

        response = requests.get(self.URL_SEARCH, params=params, headers=self._bearer_header())
        if response.status_code != 200:
            logging.error(f"Twitter search failed: {response.status_code} {response.text}")
            raise Exception(f"Twitter search failed: {response.status_code}")
        return response.json()

    def post_tweet(
        self,
        text: str,
        media_ids: list[str] | None = None,
        reply_tweet_id: str | None = None,
    ) -> dict:
        payload: dict = {"text": text}
        if media_ids:
            payload["media"] = {"media_ids": media_ids}
        if reply_tweet_id:
            payload["reply"] = {"in_reply_to_tweet_id": str(reply_tweet_id)}

        response = self._oauth1_session().post(self.URL_TWEET, json=payload)
        if response.status_code != 201:
            logging.error(f"Twitter post failed: {response.status_code} {response.text}")
            raise Exception(f"Twitter post failed: {response.status_code}")

        body = response.json()
        logging.info(f"Tweet posted: {json.dumps(body, indent=4)}")
        return body
