import json
import logging
import random

import requests
from requests_oauthlib import OAuth1

from .twitter_auth import get_3_legged_auth_client, get_twitter_oauth1_client, CONSUMER_KEY, CONSUMER_SECRET, \
    BOT_ACCESS_TOKEN, BOT_ACCESS_TOKEN_SECRET, get_bearer_auth_header
from .. import constants
from ..constants import SEARCH_TERMS_WEDNESDAY_HASHTAGS
from ..date_helper import is_it_wednesday_somewhere, seconds_until_next_earliest_wednesday

URL_TWITTER_TWEET_RESOURCE = "https://api.twitter.com/2/tweets"
URL_TWITTER_TWEET_SEARCH = "https://api.twitter.com/2/tweets/search/recent"
URL_TWITTER_MEDIA_UPLOAD = 'https://upload.twitter.com/1.1/media/upload.json'
request_token_url = "https://api.twitter.com/oauth/request_token"
base_authorization_url = "https://api.twitter.com/oauth/authorize"
access_token_url = "https://api.twitter.com/oauth/access_token"

URL_OAUTH2_BEARER_TOKEN = 'https://api.twitter.com/oauth2/token'

OAUTH1 = OAuth1(
    client_key=CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=BOT_ACCESS_TOKEN,
    resource_owner_secret=BOT_ACCESS_TOKEN_SECRET,
    # defaults to signature_method=SIGNATURE_HMAC
)


def reply_for_wednesday_tweets(start_time_iso=None, since_id=None):
    max_results = None
    query = " OR ".join(SEARCH_TERMS_WEDNESDAY_HASHTAGS)

    params = {}
    if query:
        params["query"] = query

    if start_time_iso:
        if not str(start_time_iso).endswith("Z"): raise ValueError(f"start_time needs to be in value RFC3339 "
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

    response_data = response.json().get("data")
    response_meta = response.json().get("meta")
    next_token = response.json().get("next_token")
    result_count_ = response_meta['result_count']

    if next_token:
        logging.warning(f"next_token found, but response pagination is not setup! "
                        f" next_token:{next_token}"
                        f" params: {params}"
                        f" meta:{response_meta}")

    logging.info(f"Found {result_count_} new #wednesday tweets")

    if not result_count_:
        return response_meta

    eligible_tweets = list(filter(lambda original_tweet: {
        (not original_tweet.get('possibly_sensitive')
         and original_tweet.get("reply_settings") == 'everyone')
    }, response_data))

    logging.info(f"responding to {len(eligible_tweets)} eligible #wednesday tweets")

    tweet_ids_of_errors = []
    for tweet in eligible_tweets:
        try:
            reply_to_wednesday_tweet(tweet)
        except Exception:
            tweet_ids_of_errors.append(tweet.get("id"))
            eligible_tweets.remove(tweet)
            logging.exception(f"Unable to reply_to_wednesday_tweet for tweet:{tweet.get('id')}")

    logging.info(f"Finished responding to tweets: {[x['id'] for x in eligible_tweets]}")
    if tweet_ids_of_errors:
        logging.error(f"Errors responding to tweets: {tweet_ids_of_errors}")

    return response_meta


def reply_to_wednesday_tweet(tweet):
    tweet_id_to_reply_to = tweet.get("id") or None

    if not tweet_id_to_reply_to:
        return

    is_wednesday_somewhere = is_it_wednesday_somewhere()
    message = None
    if is_wednesday_somewhere:
        message = "Yes, it is Wednesday somewhere."
    else:
        seconds_until_wednesday = seconds_until_next_earliest_wednesday()

        minutes_until = seconds_until_wednesday // 60
        hours_until = minutes_until // 60
        days_until = hours_until // 24

        if days_until > 0:
            number_used = days_until
            unit = "day" if days_until == 1 else "days"
            message = f"Still {number_used} {unit} until Wednesday."
        elif hours_until > 0:
            number_used = hours_until
            unit = "hour" if hours_until == 1 else "hours"
            message = f"We're {number_used} {unit} away until Earth hits Wednesday."
        elif minutes_until > 0:
            number_used = minutes_until
            unit = "minute" if minutes_until == 1 else "minutes"
            message = f"Earth is just {number_used} {unit} from Wednesday."
        else:
            number_used = seconds_until_wednesday
            unit = "second" if seconds_until_wednesday == 1 else "seconds"
            message = f"Buckle up! {number_used} {unit} until Earth enters Wednesday."

    post_tweet(text=message, media_ids=None, reply_tweet_id=tweet_id_to_reply_to)


def post_non_wednesday_tweet():
    message = random.choice(constants.MESSAGES_NOT_WEDNESDAY)
    post_tweet(text=message)


def post_wednesday_tweet():
    message = random.choice(constants.MESSAGES_ITS_WEDNESDAY)
    post_tweet(text=message,
               media_ids=[constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY])


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

    # auth = tweepy.AppAuthHandler(consumer_key=CONSUMER_KEY,
    #                              consumer_secret=CONSUMER_SECRET)
    #
    # response = oauth_client.media_upload(filename="../assets/captain-its-wednesday.jpeg",
    #                                          file=file_to_upload,
    #                                          media_category="tweet_image")

    # tweepy.Client.create_tweet()

    # def upload_image_to_twitter(image_binary):
    #     # auth = HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET)
    #     # client = BackendApplicationClient(client_id=CONSUMER_KEY)
    #     # oauth2 = OAuth2Session(client=client)
    #     # token_response = oauth2.fetch_token(token_url=URL_OAUTH2_BEARER_TOKEN, auth=auth)
    #     # bearer_token = token_response["access_token"]
    #     #
    #     # response = requests.post(url=URL_TWITTER_MEDIA_UPLOAD,
    #     #                        data={
    #     #                            # 'command': 'INIT',
    #     #                            'media_type': 'image/jpeg',
    #     #                            'media': image_binary,
    #     #                            'media_category': 'tweet_image'
    #     #                        },
    #     #                        headers={"Authorization": f"Bearer {bearer_token}"}
    #     #                        )
    #
    #     # TODO try to do bearbones Basic Auth, this POST was not working correcting,
    #     # username_password = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    #     # bytes_encoded = username_password.encode("utf-8")
    #     # base64_username_password = base64.b64encode(bytes_encoded)
    #     #
    #     # print(bytes_encoded)
    #     # print(base64_username_password)
    #     # asdf = requests.post(url=URL_OAUTH2_BEARER_TOKEN,
    #     #                      data={"grant_type": "client_credentials"},
    #     #                      headers={"Authorization": f"Basic {base64_username_password}"
    #     #                      'Content-Type': 'application/x-www-form-urlencoded'
    #     #                      })

    logging.info(response.status_code)
    logging.info(response.json())
