import logging
import os

from src import twitter_service, is_wednesday

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
logging.root.setLevel(LOG_LEVEL)


def lambda_handler(event, context):

    logging.info(f"event:{event}")
    logging.info(f"context:{context}")

    if is_wednesday():
        twitter_service.post_wednesday_tweet()
    else:
        twitter_service.post_non_wednesday_tweet()

