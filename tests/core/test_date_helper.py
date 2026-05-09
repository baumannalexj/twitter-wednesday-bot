import datetime
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time

from core.date_helper import (
    EARLIEST_TZ,
    LATEST_TZ,
    UTC_TZ,
    get_next_earliest_wednesday,
    get_time_min_ago,
    is_it_wednesday_somewhere,
    seconds_until_next_earliest_wednesday,
)

WEDNESDAY_MIDNIGHT_UTC = datetime.datetime.fromisoformat("2026-05-06T00:00:00Z")
EARLIEST_WEDNESDAY_MIDNIGHT = WEDNESDAY_MIDNIGHT_UTC.replace(tzinfo=EARLIEST_TZ)
LATEST_WEDNESDAY_MIDNIGHT = WEDNESDAY_MIDNIGHT_UTC.replace(tzinfo=LATEST_TZ)
EARLIEST_NEXT_WEDNESDAY_MIDNIGHT = EARLIEST_WEDNESDAY_MIDNIGHT + datetime.timedelta(weeks=1)

CHICAGO_TZ = ZoneInfo("America/Chicago")
# DST spring forward: Sunday Mar 8 2026, clocks jump 2am → 3am
CHICAGO_SPRING_FORWARD_BEFORE =\
    datetime.datetime.fromisoformat("2026-03-08T01:59:59").replace(tzinfo=CHICAGO_TZ)  # CST = UTC-6
CHICAGO_SPRING_FORWARD_AFTER  =\
    datetime.datetime.fromisoformat("2026-03-08T03:00:01").replace(tzinfo=CHICAGO_TZ)  # CDT = UTC-5
# DST fall back: Sunday Nov 1 2026, clocks fall 2am → 1am
CHICAGO_FALL_BACK_BEFORE =\
    datetime.datetime.fromisoformat("2026-11-01T01:59:59").replace(tzinfo=CHICAGO_TZ, fold=0)  # CDT = UTC-5
CHICAGO_FALL_BACK_AFTER  =\
    datetime.datetime.fromisoformat("2026-11-01T01:59:59").replace(tzinfo=CHICAGO_TZ, fold=1)  # CST = UTC-6



@pytest.mark.parametrize(
    "time,expected",
    [
        (WEDNESDAY_MIDNIGHT_UTC, True),
        (EARLIEST_WEDNESDAY_MIDNIGHT, True),
        (LATEST_WEDNESDAY_MIDNIGHT, True),
        (LATEST_WEDNESDAY_MIDNIGHT + datetime.timedelta(days=1), False),
        (EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(seconds=1), False),
    ],
)
def test_is_wednesday_somewhere_boundaries(time, expected):
    with freeze_time(time):
        assert is_it_wednesday_somewhere() is expected


@pytest.mark.parametrize(
    "time,expected",
    [
        (WEDNESDAY_MIDNIGHT_UTC, EARLIEST_NEXT_WEDNESDAY_MIDNIGHT),
        (EARLIEST_WEDNESDAY_MIDNIGHT, EARLIEST_NEXT_WEDNESDAY_MIDNIGHT),
        (LATEST_WEDNESDAY_MIDNIGHT, EARLIEST_NEXT_WEDNESDAY_MIDNIGHT),
        (LATEST_WEDNESDAY_MIDNIGHT + datetime.timedelta(days=1), EARLIEST_NEXT_WEDNESDAY_MIDNIGHT),
        (EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(seconds=1), EARLIEST_WEDNESDAY_MIDNIGHT),
    ],
)
def test_get_next_earliest_wednesday_lands_on_wednesday(time, expected):
    with freeze_time(time):
        result = get_next_earliest_wednesday()
        assert result == expected


@pytest.mark.parametrize("frozen_time,expected_seconds", [
    (EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(days=1, hours=2), 24*3600 + 2*3600),
    (EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(hours=2, minutes=1), 2 * 3600 + 60),
    (EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(minutes=1, seconds=58), 60 + 58),
    (EARLIEST_WEDNESDAY_MIDNIGHT - datetime.timedelta(seconds=1), 1),
])
def test_seconds_until_next_earliest_wednesday(frozen_time, expected_seconds):
    with freeze_time(frozen_time):
        assert seconds_until_next_earliest_wednesday() == expected_seconds


def test_seconds_until_next_earliest_wednesday_is_non_negative():
    with freeze_time(WEDNESDAY_MIDNIGHT_UTC + datetime.timedelta(hours=1)):
        # 550800 seconds: 24-14(Etc timezone) = 10 hours -1 hour from delta = 6 days + 9 hours
        assert seconds_until_next_earliest_wednesday() == 6*24*3600 + 9*3600


@pytest.mark.parametrize("frozen_time,expected_seconds", [
    (CHICAGO_SPRING_FORWARD_BEFORE, 2*86400 + 2*3600 + 1),
    (CHICAGO_SPRING_FORWARD_AFTER,  2*86400 + 1*3600 + 59*60 + 59),
    (CHICAGO_FALL_BACK_BEFORE,      2*86400 + 3*3600 + 1),
    (CHICAGO_FALL_BACK_AFTER,       2*86400 + 2*3600 + 1),
])
def test_seconds_until_next_earliest_wednesday_chicago_daylight_savings(frozen_time, expected_seconds):
    with freeze_time(frozen_time):
        assert seconds_until_next_earliest_wednesday() == expected_seconds


def test_get_time_min_ago_returns_expected_datetime():
    with freeze_time(WEDNESDAY_MIDNIGHT_UTC + datetime.timedelta(minutes=10)):
        dt = get_time_min_ago(minutes_ago=5)
        assert isinstance(dt, datetime.datetime)
        assert dt.isoformat().startswith("2026-05-06T00:05")
        assert dt.tzinfo == UTC_TZ # tz aware, not naive
