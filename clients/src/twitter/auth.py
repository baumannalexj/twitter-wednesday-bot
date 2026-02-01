import os

from requests_oauthlib import OAuth1Session

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
BOT_ACCESS_TOKEN = os.environ.get("BOT_ACCESS_TOKEN")
BOT_ACCESS_TOKEN_SECRET = os.environ.get("BOT_ACCESS_TOKEN_SECRET")

base_authorization_url = "https://api.twitter.com/oauth/authorize"
access_token_url = "https://api.twitter.com/oauth/access_token"

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token"


def get_bearer_auth_header():
    if BEARER_TOKEN is None:
        raise ValueError("No bearer token env var")
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}


def get_3_legged_auth_client():
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)
    # Get authorization
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")
    # Get the access token
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]
    # Make the request
    final_oauth_client = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    return final_oauth_client


def get_twitter_oauth1_client():
    # TODO can also just making the auth header, then request(... auth=OAUTH1)

    oauth1_session_client = OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=BOT_ACCESS_TOKEN,
        resource_owner_secret=BOT_ACCESS_TOKEN_SECRET,
        # defaults to signature_method=SIGNATURE_HMAC
    )

    return oauth1_session_client
