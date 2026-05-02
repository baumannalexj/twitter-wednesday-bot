import math
import random

from core import constants
from core.date_helper import is_it_wednesday_somewhere, seconds_until_next_earliest_wednesday


def build_wednesday_reply(tweet):
    """Returns (message, tweet_id) tuple, or (None, None) if tweet has no id."""
    tweet_id = tweet.get("id") or None
    if not tweet_id:
        return None, None

    if is_it_wednesday_somewhere():
        return "Yes, it is Wednesday somewhere.", tweet_id

    seconds_until_wednesday = seconds_until_next_earliest_wednesday()
    minutes_until = math.floor(seconds_until_wednesday // 60)
    hours_until = math.floor(minutes_until // 60)
    days_until = math.floor(hours_until // 24)

    if days_until > 0:
        unit = "day" if days_until == 1 else "days"
        message = f"Still {days_until} {unit} and {hours_until % 24} hours until Earth sees Wednesday."
    elif hours_until > 1:
        unit = "hour" if hours_until == 1 else "hours"
        message = f"We're {hours_until} {unit} and {minutes_until % 60} minutes away until Earth hits Wednesday."
    elif minutes_until > 1:
        unit = "minute" if minutes_until == 1 else "minutes"
        message = f"Earth is just {minutes_until} {unit} and {seconds_until_wednesday % 60} seconds from Wednesday."
    else:
        unit = "second" if seconds_until_wednesday == 1 else "seconds"
        message = f"Buckle up! {seconds_until_wednesday} {unit} until Earth enters Wednesday."

    return message, tweet_id


def pick_wednesday_message():
    return random.choice(constants.MESSAGES_ITS_WEDNESDAY)


def pick_non_wednesday_message():
    return random.choice(constants.MESSAGES_NOT_WEDNESDAY)
