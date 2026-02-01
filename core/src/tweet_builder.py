import math
import random

from core import constants
from core.date_helper import is_it_wednesday_somewhere, seconds_until_next_earliest_wednesday


def build_wednesday_reply(tweet):
    """Build a reply message for a tweet asking about Wednesday.
    Returns (message, tweet_id) tuple, or (None, None) if tweet has no id."""
    tweet_id = tweet.get("id") or None

    if not tweet_id:
        return None, None

    is_wednesday_somewhere = is_it_wednesday_somewhere()
    message = None
    if is_wednesday_somewhere:
        message = "Yes, it is Wednesday somewhere."
    else:
        seconds_until_wednesday = seconds_until_next_earliest_wednesday()

        minutes_until = math.floor(seconds_until_wednesday // 60)
        hours_until = math.floor(minutes_until // 60)
        days_until = math.floor(hours_until // 24)

        if days_until > 0:
            number_used = days_until
            unit = "day" if days_until == 1 else "days"
            message = f"Still {number_used} {unit} and {hours_until % 24} hours until Earth sees Wednesday."
        elif hours_until > 1:
            number_used = hours_until
            unit = "hour" if hours_until == 1 else "hours"
            message = f"We're {number_used} {unit}" \
                      f" and {minutes_until % 60} minutes away until Earth hits Wednesday."
        elif minutes_until > 1:
            number_used = minutes_until
            unit = "minute" if minutes_until == 1 else "minutes"
            message = f"Earth is just {number_used} {unit} and {seconds_until_wednesday % 60} seconds from Wednesday."
        else:
            number_used = seconds_until_wednesday
            unit = "second" if seconds_until_wednesday == 1 else "seconds"
            message = f"Buckle up! {number_used} {unit} until Earth enters Wednesday."

    return message, tweet_id


def pick_wednesday_message():
    return random.choice(constants.MESSAGES_ITS_WEDNESDAY)


def pick_non_wednesday_message():
    return random.choice(constants.MESSAGES_NOT_WEDNESDAY)
