import datetime
import math
from zoneinfo import ZoneInfo

DOW_WEDNESDAY = 3
EARLIEST_TZ = ZoneInfo("Etc/GMT-14")  # GMT+14 is the earliest TZ. Note: the Etc standard uses negatives
LAST_TZ = ZoneInfo("Etc/GMT+12")  # GMT-12 is the last TZ before the IDL. Note: the Etc standard uses negatives
MINUTES_LAMBDA_TIMEOUT = 2


def get_next_earliest_wednesday():
    the_first_next_wed = datetime.datetime.now(tz=EARLIEST_TZ)
    while the_first_next_wed.isoweekday() != DOW_WEDNESDAY:
        the_first_next_wed += datetime.timedelta(days=1)

    return the_first_next_wed


def is_wednesday_for_tz(tz_offset=EARLIEST_TZ):
    return datetime.datetime.now(tz=tz_offset).isoweekday() == DOW_WEDNESDAY


def is_it_wednesday_somewhere():
    return is_wednesday_for_tz(EARLIEST_TZ) or is_wednesday_for_tz(LAST_TZ)


def get_time_min_ago(minutes_ago=MINUTES_LAMBDA_TIMEOUT):
    time_ago = datetime.datetime.now() - datetime.timedelta(minutes=minutes_ago)
    return time_ago


def seconds_until_next_earliest_wednesday():
    """check if it's wednesday somewhere first before calculating this,
    this method doesn't take into account if you are currently in Wed, but GMT+14 is now Thursday"""
    the_first_next_wed = get_next_earliest_wednesday()

    return math.floor(
        (the_first_next_wed - datetime.datetime.now(tz=EARLIEST_TZ)).total_seconds()
    )


if __name__ == "__main__":
    get_next_earliest_wednesday()