import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from clients.aws.ssm_client import get_parameter_datetime, put_parameter_datetime
from core.constants import SEARCH_TERMS_WEDNESDAY_HASHTAGS
from core.date_helper import get_time_min_ago, MINUTES_LAMBDA_TIMEOUT
from core.tweet_builder import build_wednesday_reply
from clients.twitter.tweet_client import search_recent_tweets, post_tweet

SSM_PARAM_NAME = "param-store-db-social-listening"
RATE_LIMIT_INTERVAL = timedelta(hours=10)

def handler(event, context):

    logging.info(f"event:{event}")
    logging.info(f"context:{context}")

    if should_skip_invocation():
        return

    start = get_time_min_ago(MINUTES_LAMBDA_TIMEOUT)
    start_iso = start.isoformat() + "Z"

    logging.info(f"Replying to wednesday tweets since {start_iso}")
    reply_for_wednesday_tweets(start_time_iso=start_iso)


def get_last_invocation_datetime() -> Optional[datetime]:
    return get_parameter_datetime(SSM_PARAM_NAME)


def set_last_invocation_datetime(dt: datetime) -> None:
    put_parameter_datetime(SSM_PARAM_NAME, dt)


def should_skip_invocation() -> bool:
    now: datetime = datetime.now(timezone.utc)
    last_invocation_datetime: Optional[datetime] = get_last_invocation_datetime()

    set_last_invocation_datetime(now)

    if last_invocation_datetime and (now - last_invocation_datetime) < RATE_LIMIT_INTERVAL:
        next_check: datetime = last_invocation_datetime + RATE_LIMIT_INTERVAL
        logging.info(
            f"Last invocation was at {last_invocation_datetime.isoformat()}. "
            f"Twitter only allows 100 reads a month, "
            f"waiting until {next_check.isoformat()} to check for wednesday hashtags."
        )
        return True

    return False





def reply_for_wednesday_tweets(start_time_iso=None, since_id=None):
    query = " OR ".join(SEARCH_TERMS_WEDNESDAY_HASHTAGS)

    response_json = search_recent_tweets(query=query, start_time_iso=start_time_iso, since_id=since_id)

    response_data = response_json.get("data")
    response_meta = response_json.get("meta")
    next_token = response_json.get("next_token")
    result_count_ = response_meta['result_count']

    if next_token:
        logging.warning(f"next_token found, but response pagination is not setup! "
                        f" next_token:{next_token}"
                        f" params: query={query}, start_time_iso={start_time_iso}, since_id={since_id}"
                        f" meta:{response_meta}")

    logging.info(f"Found {result_count_} new #wednesday tweets")

    if not result_count_:
        return response_meta

    eligible_tweets = list(filter(lambda original_tweet: {
        (not original_tweet.get('possibly_sensitive')
         and original_tweet.get("reply_settings") == 'everyone')
    }, response_data))

    logging.info(f"responding to {len(eligible_tweets)} eligible #wednesday tweets")

    tweet_ids_of_errors = []
    for tweet in eligible_tweets:
        try:
            message, tweet_id = build_wednesday_reply(tweet)
            if message and tweet_id:
                post_tweet(text=message, reply_tweet_id=tweet_id)
        except Exception:
            tweet_ids_of_errors.append(tweet.get("id"))
            eligible_tweets.remove(tweet)
            logging.exception(f"Unable to reply_to_wednesday_tweet for tweet:{tweet.get('id')}")

    logging.info(f"Finished responding to tweets: {[x['id'] for x in eligible_tweets]}")
    if tweet_ids_of_errors:
        logging.error(f"Errors responding to tweets: {tweet_ids_of_errors}")

    return response_meta


if __name__ == '__main__':
    handler(event={"should_set_rules": False}, context=None)