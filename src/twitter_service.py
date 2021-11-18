import json
import logging
import os
import random

from requests_oauthlib import OAuth1Session, OAuth1

from src import constants
from src.twitter_auth import get_3_legged_auth_client

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
BOT_ACCESS_TOKEN = os.environ.get("BOT_ACCESS_TOKEN")
BOT_ACCESS_TOKEN_SECRET = os.environ.get("BOT_ACCESS_TOKEN_SECRET")

URL_TWITTER_TWEET_RESOURCE = "https://api.twitter.com/2/tweets"
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


def _get_twitter_client():
    # TODO can also just making the auth header, then request(... auth=OAUTH1)

    oauth1_session_client = OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=BOT_ACCESS_TOKEN,
        resource_owner_secret=BOT_ACCESS_TOKEN_SECRET,
        # defaults to signature_method=SIGNATURE_HMAC
    )

    return oauth1_session_client


def post_non_wednesday_tweet():
    message = random.choice(constants.MESSAGES_NOT_WEDNESDAY)
    post_tweet(text=message)


def post_wednesday_tweet():
    message = random.choice(constants.MESSAGES_ITS_WEDNESDAY)
    post_tweet(text=message,
               media_ids=[constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY])


def post_tweet(text: str = "Hello!", media_ids: [str] = None):
    payload = {}
    if text:
        payload["text"] = text

    if media_ids:
        payload["media"] = {"media_ids": media_ids}

    client = _get_twitter_client()

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
