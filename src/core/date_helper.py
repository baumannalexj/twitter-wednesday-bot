import datetime
import math
from zoneinfo import ZoneInfo

DAY_OF_WEEK_WEDNESDAY = 3
EARLIEST_TZ = ZoneInfo("Etc/GMT-14")  # GMT+14 — first to enter Wednesday
LAST_TZ = ZoneInfo("Etc/GMT+12")  # GMT-12 — last to leave Wednesday
MINUTES_LAMBDA_TIMEOUT = 2


def get_next_earliest_wednesday() -> datetime.datetime:
    the_first_next_wed = datetime.datetime.now(tz=EARLIEST_TZ)
    while the_first_next_wed.isoweekday() != DAY_OF_WEEK_WEDNESDAY:
        the_first_next_wed += datetime.timedelta(days=1)
    return the_first_next_wed


def is_wednesday_for_tz(tz_offset: ZoneInfo = EARLIEST_TZ) -> bool:
    return datetime.datetime.now(tz=tz_offset).isoweekday() == DAY_OF_WEEK_WEDNESDAY


def is_it_wednesday_somewhere() -> bool:
    return is_wednesday_for_tz(EARLIEST_TZ) or is_wednesday_for_tz(LAST_TZ)


def get_time_min_ago(minutes_ago: int = MINUTES_LAMBDA_TIMEOUT) -> datetime.datetime:
    return datetime.datetime.now() - datetime.timedelta(minutes=minutes_ago)


def seconds_until_next_earliest_wednesday() -> int:
    """Seconds until GMT+14 hits Wednesday. Caller should check is_it_wednesday_somewhere() first."""
    the_first_next_wed = get_next_earliest_wednesday()
    return math.floor((the_first_next_wed - datetime.datetime.now(tz=EARLIEST_TZ)).total_seconds())
