import datetime
import math
from zoneinfo import ZoneInfo

DAY_OF_WEEK_WEDNESDAY_ISO = 3
EARLIEST_TZ = ZoneInfo("Etc/GMT-14")  # GMT+14 — first to enter Wednesday
LATEST_TZ = ZoneInfo("Etc/GMT+12")  # GMT-12 — last to leave Wednesday
UTC_TZ = ZoneInfo("UTC")
MINUTES_LAMBDA_TIMEOUT = 2


def get_next_earliest_wednesday() -> datetime.datetime:
    now = datetime.datetime.now(tz=EARLIEST_TZ)
    days_until_wednesday = (DAY_OF_WEEK_WEDNESDAY_ISO - now.isoweekday()) % 7 or 7
    return ((now + datetime.timedelta(days=days_until_wednesday))
            .replace(hour=0,minute=0, second=0, microsecond=0))


def is_wednesday_for_tz(tz_offset) -> bool:
    return datetime.datetime.now(tz=tz_offset).isoweekday() == DAY_OF_WEEK_WEDNESDAY_ISO


def is_it_wednesday_somewhere() -> bool:
    return is_wednesday_for_tz(EARLIEST_TZ) or is_wednesday_for_tz(LATEST_TZ)


def get_time_min_ago(minutes_ago: int = MINUTES_LAMBDA_TIMEOUT) -> datetime.datetime:
    return datetime.datetime.now(tz=UTC_TZ) - datetime.timedelta(minutes=minutes_ago)


def seconds_until_next_earliest_wednesday() -> int:
    """Seconds until GMT+14 hits Wednesday. Caller should check is_it_wednesday_somewhere() first."""
    the_first_next_wed = get_next_earliest_wednesday()
    return math.floor((the_first_next_wed - datetime.datetime.now(tz=UTC_TZ)).total_seconds())
