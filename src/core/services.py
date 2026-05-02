import logging
import math
import random

from clients.twitter import TwitterClient
from core import constants
from core.date_helper import (
    is_it_wednesday_somewhere,
    is_wednesday_for_tz,
    seconds_until_next_earliest_wednesday,
)


class WednesdayService:
    def __init__(self, twitter_client: TwitterClient):
        self._twitter = twitter_client

    def post_for_today(self) -> None:
        """Post a Wednesday or non-Wednesday message based on current time."""
        if is_wednesday_for_tz():
            self._twitter.post_tweet(
                text=random.choice(constants.MESSAGES_ITS_WEDNESDAY),
                media_ids=[constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY],
            )
        else:
            self._twitter.post_tweet(text=random.choice(constants.MESSAGES_NOT_WEDNESDAY))

    def reply_to_recent_wednesday_tweets(self, start_time_iso: str) -> dict:
        """Search for recent #wednesday-tagged tweets and reply to each eligible one."""
        query = " OR ".join(constants.SEARCH_TERMS_WEDNESDAY_HASHTAGS)
        response = self._twitter.search_recent_tweets(query=query, start_time_iso=start_time_iso)

        meta = response.get("meta", {})
        result_count = meta.get("result_count", 0)

        if response.get("next_token"):
            logging.warning(f"next_token present but pagination not implemented. meta:{meta}")

        logging.info(f"Found {result_count} new #wednesday tweets")
        if not result_count:
            return meta

        eligible = [
            t
            for t in response.get("data", [])
            if not t.get("possibly_sensitive") and t.get("reply_settings") == "everyone"
        ]
        logging.info(f"Replying to {len(eligible)} eligible tweets")

        replied, errors = [], []
        for tweet in eligible:
            try:
                message, tweet_id = self._build_reply(tweet)
                if message and tweet_id:
                    self._twitter.post_tweet(text=message, reply_tweet_id=tweet_id)
                    replied.append(tweet_id)
            except Exception:
                errors.append(tweet.get("id"))
                logging.exception(f"Failed to reply to tweet:{tweet.get('id')}")

        logging.info(f"Replied to: {replied}")
        if errors:
            logging.error(f"Failed: {errors}")
        return meta

    def _build_reply(self, tweet: dict) -> tuple[str | None, str | None]:
        tweet_id = tweet.get("id") or None
        if not tweet_id:
            return None, None

        if is_it_wednesday_somewhere():
            return "Yes, it is Wednesday somewhere.", tweet_id

        seconds = seconds_until_next_earliest_wednesday()
        minutes = math.floor(seconds // 60)
        hours = math.floor(minutes // 60)
        days = math.floor(hours // 24)

        if days > 0:
            unit = "day" if days == 1 else "days"
            message = f"Still {days} {unit} and {hours % 24} hours until Earth sees Wednesday."
        elif hours > 1:
            unit = "hour" if hours == 1 else "hours"
            message = (
                f"We're {hours} {unit} and {minutes % 60} minutes away until Earth hits Wednesday."
            )
        elif minutes > 1:
            unit = "minute" if minutes == 1 else "minutes"
            message = f"Earth is just {minutes} {unit} and {seconds % 60} seconds from Wednesday."
        else:
            unit = "second" if seconds == 1 else "seconds"
            message = f"Buckle up! {seconds} {unit} until Earth enters Wednesday."

        return message, tweet_id
