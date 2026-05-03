import datetime

import pytest
from freezegun import freeze_time

from core.date_helper import (
    UTC_TZ,
    get_next_earliest_wednesday,
    get_time_min_ago,
    is_it_wednesday_somewhere,
    seconds_until_next_earliest_wednesday,
)

# Centralized times dictionary for parametrized tests
TIMES = {
    "wednesday_midnight": "2025-01-01T00:00:00Z",
    "thursday_midnight": "2025-01-02T00:00:00Z",
    "tuesday_midnight": "2025-01-07T00:00:00Z",
    "wednesday_0010": "2025-01-01T00:10:00Z",
}

ISITWEDNESDAY_TIMES = {
    # 1 second before GMT+14 hits Wednesday (Tuesday 09:59:59 UTC)
    "one_sec_before_earliest": "2024-12-31T09:59:59Z",
    # Exactly midnight GMT+14 (Tuesday 10:00:00 UTC)
    "midnight_earliest": "2024-12-31T10:00:00Z",
    # Exactly midnight GMT-12 (Wednesday 12:00:00 UTC)
    # Note: At this moment, it's Wednesday in ONLY one spot (the last spot)
    "midnight_latest": "2025-01-01T12:00:00Z",
    # 1 second after GMT-12 leaves Wednesday (Thursday 12:00:01 UTC)
    "one_sec_after_latest": "2025-01-02T12:00:01Z",
    # Standard UTC mid-week check
    "wednesday_utc_noon": "2025-01-01T12:00:00Z",
}


@pytest.mark.parametrize(
    "key,expected",
    [
        ("one_sec_before_earliest", False),
        ("midnight_earliest", True),
        ("wednesday_utc_noon", True),
        # This is the split second GMT-12 enters Wednesday.
        # It's still Wednesday "somewhere" until Thursday 12:00:00 UTC.
        ("midnight_latest", True),
        ("one_sec_after_latest", False),
    ],
)
def test_is_wednesday_somewhere_boundaries(key, expected):
    with freeze_time(ISITWEDNESDAY_TIMES[key]):
        assert is_it_wednesday_somewhere() is expected


@pytest.mark.parametrize(
    "key,expected",
    [
        ("wednesday_midnight", True),
        ("tuesday_midnight", False),
    ],
)
def test_is_it_wednesday_somewhere_param(key, expected):
    with freeze_time(TIMES[key]):
        assert is_it_wednesday_somewhere() is expected


def test_get_next_earliest_wednesday_lands_on_wednesday():
    with freeze_time(TIMES["wednesday_midnight"]):
        result = get_next_earliest_wednesday()
        assert result.isoweekday() == 3


def test_seconds_until_next_earliest_wednesday_is_non_negative():
    with freeze_time(TIMES["wednesday_midnight"]):
        assert seconds_until_next_earliest_wednesday() >= 0


def test_get_time_min_ago_returns_expected_datetime():
    with freeze_time(TIMES["wednesday_0010"]):
        dt = get_time_min_ago(minutes_ago=5)
        assert isinstance(dt, datetime.datetime)
        assert dt.isoformat().startswith("2025-01-01T00:05")
        # ensure the result is timezone-aware and in UTC
        assert dt.tzinfo == UTC_TZ
