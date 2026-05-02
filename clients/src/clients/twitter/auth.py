import os

from requests_oauthlib import OAuth1Session

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
BOT_ACCESS_TOKEN = os.environ.get("BOT_ACCESS_TOKEN")
BOT_ACCESS_TOKEN_SECRET = os.environ.get("BOT_ACCESS_TOKEN_SECRET")

base_authorization_url = "https://api.twitter.com/oauth/authorize"
access_token_url = "https://api.twitter.com/oauth/access_token"
request_token_url = "https://api.twitter.com/oauth/request_token"


def get_bearer_auth_header():
    if BEARER_TOKEN is None:
        raise ValueError("No bearer token env var")
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}


def get_twitter_oauth1_client():
    return OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=BOT_ACCESS_TOKEN,
        resource_owner_secret=BOT_ACCESS_TOKEN_SECRET,
    )
