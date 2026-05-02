import json
import logging

import requests

from clients.twitter.auth import get_bearer_auth_header, get_twitter_oauth1_client

URL_TWITTER_TWEET_RESOURCE = "https://api.twitter.com/2/tweets"
URL_TWITTER_TWEET_SEARCH = "https://api.twitter.com/2/tweets/search/recent"


def search_recent_tweets(query, start_time_iso=None, since_id=None, max_results=None):
    params = {"query": query}

    if start_time_iso:
        if not str(start_time_iso).endswith("Z"):
            raise ValueError(f"start_time must be RFC3339 (iso+'Z'): {start_time_iso}")
        params["start_time"] = start_time_iso

    if since_id:
        params["since_id"] = since_id

    if max_results:
        params["max_results"] = max_results

    response = requests.get(
        url=URL_TWITTER_TWEET_SEARCH,
        params=params,
        headers=get_bearer_auth_header(),
    )

    if response.status_code != 200:
        logging.error(f"Error searching tweets: {response.status_code} {response.text}")
        raise Exception(f"Error searching tweets: {response.status_code}")

    return response.json()


def post_tweet(text: str = "Hello!", media_ids: list[str] = None, reply_tweet_id=None):
    payload = {"text": text}

    if media_ids:
        payload["media"] = {"media_ids": media_ids}

    if reply_tweet_id:
        payload["reply"] = {"in_reply_to_tweet_id": str(reply_tweet_id)}

    client = get_twitter_oauth1_client()
    response = client.post(URL_TWITTER_TWEET_RESOURCE, json=payload)

    if response.status_code != 201:
        logging.error(f"Error posting tweet: {response.status_code} {response.text}")
        raise Exception(f"Error posting tweet: {response.status_code}")

    logging.info(f"Tweet posted: {json.dumps(response.json(), indent=4)}")
