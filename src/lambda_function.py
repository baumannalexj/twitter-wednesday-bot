import logging
import os

from . import is_wednesday_for_tz
from .twitter import twitter_service

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
logging.root.setLevel(LOG_LEVEL)


def lambda_handler(event, context):

    logging.info(f"event:{event}")
    logging.info(f"context:{context}")

    if is_wednesday_for_tz():
        twitter_service.post_wednesday_tweet()
    else:
        twitter_service.post_non_wednesday_tweet()
