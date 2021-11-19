import logging
from time import sleep

from ..date_helper import get_time_min_ago, MINUTES_LAMBDA_TIMEOUT
from ..twitter.twitter_service import reply_for_wednesday_tweets


def handler(event, context):

    logging.info(f"event:{event}")
    logging.info(f"context:{context}")
    start = get_time_min_ago(MINUTES_LAMBDA_TIMEOUT)
    start_iso = start.isoformat() + "Z"
    logging.info(f"Replying to wednesday tweets since {start_iso}")
    reply_for_wednesday_tweets(start_time_iso=start_iso)

    # TODO just running once every MINUTES_LAMBDA_TIMEOUT now,
    #  would like to setup a lambda that stays running for 10 min, and loops over from last id,
    #  but edge cases: first scan is from start time, but nothing returns -- do we keep going until we get a "last_id",
    #  but only update last_id if another one is returned -- what to do

    latest_id = None
    # while True:
    #     """will timeout from lambda"""
    #     if latest_id:
    #         meta = reply_for_wednesday_tweets(since_id=latest_id)
    #     else:
    #         start = get_time_min_ago(MINUTES_LAMBDA_TIMEOUT)
    #         start_iso = start.isoformat() + "Z"
    #         logging.info(f"Replying to wednesday tweets since {start_iso}")
            # meta = reply_for_wednesday_tweets(start_time_iso=start_iso)
        # latest_id = meta.get("oldest_id") or latest_id

        # sleep(3_000)


if __name__ == '__main__':
    handler(event={"should_set_rules": False}, context=None)