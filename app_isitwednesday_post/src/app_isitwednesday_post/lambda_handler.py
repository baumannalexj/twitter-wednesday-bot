import logging
import os

from clients.twitter.tweet_client import post_tweet
from core import constants
from core.date_helper import is_wednesday_for_tz
from core.tweet_builder import pick_wednesday_message, pick_non_wednesday_message

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.root.setLevel(LOG_LEVEL)


def lambda_handler(event, context):
    logging.info(f"event:{event}")

    if is_wednesday_for_tz():
        post_tweet(
            text=pick_wednesday_message(),
            media_ids=[constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY],
        )
    else:
        post_tweet(text=pick_non_wednesday_message())
