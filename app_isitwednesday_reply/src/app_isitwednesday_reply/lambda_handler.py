import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from clients.aws.ssm_client import get_parameter_datetime, put_parameter_datetime
from clients.twitter.tweet_client import search_recent_tweets, post_tweet
from core.constants import SEARCH_TERMS_WEDNESDAY_HASHTAGS
from core.date_helper import get_time_min_ago, MINUTES_LAMBDA_TIMEOUT
from core.tweet_builder import build_wednesday_reply

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.root.setLevel(LOG_LEVEL)

SSM_PARAM_NAME = "param-store-db-social-listening"
RATE_LIMIT_INTERVAL = timedelta(hours=10)


def lambda_handler(event, context):
    logging.info(f"event:{event}")

    if _should_skip_invocation():
        return

    start_iso = get_time_min_ago(MINUTES_LAMBDA_TIMEOUT).isoformat() + "Z"
    logging.info(f"Replying to wednesday tweets since {start_iso}")
    _reply_for_wednesday_tweets(start_time_iso=start_iso)


def _should_skip_invocation() -> bool:
    now = datetime.now(timezone.utc)
    last: Optional[datetime] = get_parameter_datetime(SSM_PARAM_NAME)
    put_parameter_datetime(SSM_PARAM_NAME, now)

    if last and (now - last) < RATE_LIMIT_INTERVAL:
        next_check = last + RATE_LIMIT_INTERVAL
        logging.info(
            f"Last invocation at {last.isoformat()}. "
            f"Skipping until {next_check.isoformat()} to stay within Twitter read limits."
        )
        return True
    return False


def _reply_for_wednesday_tweets(start_time_iso=None, since_id=None):
    query = " OR ".join(SEARCH_TERMS_WEDNESDAY_HASHTAGS)
    response_json = search_recent_tweets(query=query, start_time_iso=start_time_iso, since_id=since_id)

    response_data = response_json.get("data")
    response_meta = response_json.get("meta")
    result_count = response_meta["result_count"]

    if response_json.get("next_token"):
        logging.warning(f"next_token present but pagination not implemented. meta:{response_meta}")

    logging.info(f"Found {result_count} new #wednesday tweets")

    if not result_count:
        return response_meta

    eligible_tweets = [
        t for t in response_data
        if not t.get("possibly_sensitive") and t.get("reply_settings") == "everyone"
    ]
    logging.info(f"Responding to {len(eligible_tweets)} eligible tweets")

    errors = []
    replied = []
    for tweet in eligible_tweets:
        try:
            message, tweet_id = build_wednesday_reply(tweet)
            if message and tweet_id:
                post_tweet(text=message, reply_tweet_id=tweet_id)
                replied.append(tweet_id)
        except Exception:
            errors.append(tweet.get("id"))
            logging.exception(f"Failed to reply to tweet:{tweet.get('id')}")

    logging.info(f"Replied to: {replied}")
    if errors:
        logging.error(f"Failed tweets: {errors}")

    return response_meta
