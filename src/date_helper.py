import datetime
from zoneinfo import ZoneInfo

DOW_WEDNESDAY = 3
EARLIEST_TZ = ZoneInfo("Etc/GMT-14")  # GMT+14 is the earlier TZ, the Etc standard uses negatives though


def is_wednesday(tz_offset=EARLIEST_TZ):
    return datetime.datetime.now(tz=tz_offset).isoweekday() == DOW_WEDNESDAY
