import logging

from core import wednesday_service
from core.date_helper import MINUTES_LAMBDA_TIMEOUT, get_time_min_ago


def handler(event, context):
    logging.info(f"event:{event}")
    start_iso = get_time_min_ago(MINUTES_LAMBDA_TIMEOUT).isoformat() + "Z"
    logging.info(f"Replying to wednesday tweets since {start_iso}")
    wednesday_service.reply_to_recent_wednesday_tweets(start_time_iso=start_iso)


if __name__ == "__main__":
    handler(event={}, context=None)
