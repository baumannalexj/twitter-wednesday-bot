import logging
import os

from clients.src.twitter.tweet_client import post_tweet
from core.src import constants
from core.src.date_helper import is_wednesday_for_tz
from core.src.tweet_builder import pick_wednesday_message, pick_non_wednesday_message

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
logging.root.setLevel(LOG_LEVEL)


def lambda_handler(event, context):

    logging.info(f"event:{event}")
    logging.info(f"context:{context}")

    if is_wednesday_for_tz():
        message = pick_wednesday_message()
        post_tweet(text=message, media_ids=[constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY])
    else:
        message = pick_non_wednesday_message()
        post_tweet(text=message)