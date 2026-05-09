import datetime
import logging
import math
import random
from dataclasses import dataclass

from core import constants
from core.date_helper import (
    is_it_wednesday_somewhere,
    seconds_until_next_earliest_wednesday,
)
from core.models.social_post import SocialPostModel, TwitterReplyModel, TwitterPostModel
from core.ports.twitter_client_port import ITwitterClient


def _build_twitter_reply(social_post: SocialPostModel) -> TwitterReplyModel:

    if is_it_wednesday_somewhere():
        return TwitterReplyModel(reply_to_id=social_post.id, message="Yes, it is Wednesday somewhere.")

    seconds = seconds_until_next_earliest_wednesday()
    minutes = math.floor(seconds // 60)
    hours = math.floor(minutes // 60)
    days = math.floor(hours // 24)

    if days > 0:
        unit = "day" if days == 1 else "days"
        message = f"Still {days} {unit} and {hours % 24} hours until Earth sees Wednesday."
    elif hours > 0:
        unit = "hour" if hours == 1 else "hours"
        message = f"We're {hours} {unit} and {minutes % 60} minutes away until Earth hits Wednesday."
    elif minutes > 0:
        unit = "minute" if minutes == 1 else "minutes"
        message = f"Earth is just {minutes} {unit} and {seconds % 60} seconds from Wednesday."
    else:
        unit = "second" if seconds == 1 else "seconds"
        message = f"Buckle up! {seconds} {unit} until Earth enters Wednesday."

    return TwitterReplyModel(reply_to_id=social_post.id, message=message)

@dataclass(frozen=True)
class PostService:
    _client: ITwitterClient

    def check_if_wednesday_and_post(self) -> SocialPostModel:
        """Post a Wednesday or non-Wednesday message based on current time."""
        if is_it_wednesday_somewhere():
            return self._client.post_tweet(
                message_string=random.choice(constants.MESSAGES_ITS_WEDNESDAY),
                media_ids=[constants.TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY],
            )
        else:
            return self._client.post_tweet(message_string=random.choice(constants.MESSAGES_NOT_WEDNESDAY))

    def reply_to_recent_wednesday_tweets(self, start_time_iso: datetime.datetime) -> None:
        """Search for recent #wednesday-tagged tweets and reply to each eligible one."""
        eligible_posts: list[SocialPostModel] = self._client.find_recent_hashtags_posts(
            hashtags_to_search=constants.SEARCH_TERMS_WEDNESDAY_HASHTAGS, start_time_iso=start_time_iso
        )
        logging.info(f"Replying to {len(eligible_posts)} eligible posts")

        replied_post_ids, error_post_ids = [], []
        for post in eligible_posts:
            try:
                twitter_reply = _build_twitter_reply(post)

                self._client.reply_to_tweet(twitter_reply)
                replied_post_ids.append(post.id)
            except Exception:
                error_post_ids.append(post.id)
                logging.exception(f"Failed to reply to tweet:{post.id}")

        logging.info(f"Replied to: {replied_post_ids}")
        if error_post_ids:
            logging.error(f"Failed: {error_post_ids}")
