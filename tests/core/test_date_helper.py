import datetime
from unittest.mock import patch

from core.date_helper import (
    EARLIEST_TZ,
    get_next_earliest_wednesday,
    is_it_wednesday_somewhere,
    is_wednesday_for_tz,
    seconds_until_next_earliest_wednesday,
)


@patch("core.date_helper.datetime")
def test_is_wednesday_for_tz_true(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(
        2025, 1, 1, 12, 0, tzinfo=EARLIEST_TZ
    )  # Wed
    assert is_wednesday_for_tz() is True


@patch("core.date_helper.datetime")
def test_is_wednesday_for_tz_false(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(
        2025, 1, 2, 12, 0, tzinfo=EARLIEST_TZ
    )  # Thu
    assert is_wednesday_for_tz() is False


@patch("core.date_helper.is_wednesday_for_tz")
def test_is_it_wednesday_somewhere_true_when_either_tz(mock_check):
    mock_check.side_effect = [False, True]
    assert is_it_wednesday_somewhere() is True


@patch("core.date_helper.is_wednesday_for_tz")
def test_is_it_wednesday_somewhere_false_when_neither(mock_check):
    mock_check.side_effect = [False, False]
    assert is_it_wednesday_somewhere() is False


def test_get_next_earliest_wednesday_lands_on_wednesday():
    result = get_next_earliest_wednesday()
    assert result.isoweekday() == 3


def test_seconds_until_next_earliest_wednesday_is_non_negative():
    assert seconds_until_next_earliest_wednesday() >= 0
