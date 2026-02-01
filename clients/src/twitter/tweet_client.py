import json
import logging

import requests

from .auth import get_bearer_auth_header

# TODO move to application config file

URL_TWITTER_TWEET_RESOURCE = "https://api.twitter.com/2/tweets"
URL_TWITTER_TWEET_SEARCH = "https://api.twitter.com/2/tweets/search/recent"
URL_TWITTER_MEDIA_UPLOAD = 'https://upload.twitter.com/1.1/media/upload.json'


def search_recent_tweets(query, start_time_iso=None, since_id=None, max_results=None):
    params = {}
    if query:
        params["query"] = query

    if start_time_iso:
        if not str(start_time_iso).endswith("Z"):
            raise ValueError(f"start_time needs to be in value RFC3339 "
                             f"(iso+'Z' w/o offset): {start_time_iso} ")
        params["start_time"] = start_time_iso

    if since_id:
        params["since_id"] = since_id

    if max_results:
        params["max_results"] = max_results

    response = requests.get(url=URL_TWITTER_TWEET_SEARCH,
                            params=params,
                            headers=get_bearer_auth_header())

    if response.status_code != 200:
        message = f"Error searching tweets for wednesday hashtags: {response.status_code} {response.text}"
        logging.error(message)
        raise Exception(message)

    return response.json()


def post_tweet(text: str = "Hello!",
               media_ids: [str] = None,
               reply_tweet_id=None):
    payload = {}
    if text:
        payload["text"] = text

    if media_ids:
        payload["media"] = {"media_ids": media_ids}

    if reply_tweet_id:
        payload["reply"] = {"in_reply_to_tweet_id": str(reply_tweet_id)}

    client = get_twitter_oauth1_client()

    response = client.post(
        URL_TWITTER_TWEET_RESOURCE,
        json=payload,
    )
    if response.status_code != 201:
        message = f"Request returned an error: {response.status_code} {response.text}"
        logging.error(message)
        raise Exception(message)

    logging.info("Response code: {}".format(response.status_code))
    # Saving the response as JSON
    json_response = response.json()
    logging.info(json.dumps(json_response, indent=4))

    # TODO persist response to dynamo
    # {
    #     "data": {
    #         "id": "1461059150570573832",
    #         "text": "eyy!"
    #     }
    # }


def upload_image_to_twitter(file_to_upload):
    """TODO either 401 or 403, can't seem to get this to work, but the image is uploaded,
    and the id is saved in constants.py"""
    oauth_client = get_3_legged_auth_client()

    image_bytes = file_to_upload.read()

    response = oauth_client.post(url=URL_TWITTER_MEDIA_UPLOAD,
                                 json={
                                     # 'command': 'INIT',
                                     'media_type': 'image/jpeg',
                                     'media': image_bytes,
                                     'media_category': 'tweet_image'
                                 })

    logging.info(response.status_code)
    logging.info(response.json())
