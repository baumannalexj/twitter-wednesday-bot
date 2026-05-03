import logging

from app_isitwednesday_reply import app
from core.date_helper import MINUTES_LAMBDA_TIMEOUT, get_time_min_ago


def lambda_handler(event, context):
    logging.info(f"{event=}")
    start_time = get_time_min_ago(MINUTES_LAMBDA_TIMEOUT)
    logging.info(f"Replying to wednesday tweets since {start_time.isoformat()}")
    app.wednesday_service.reply_to_recent_wednesday_tweets(start_time_iso=start_time)
