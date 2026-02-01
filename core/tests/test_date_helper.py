from core.date_helper import is_wednesday_for_tz


def test_is_wednesday_for_tz_returns_bool():
    result = is_wednesday_for_tz()
    assert isinstance(result, bool)
