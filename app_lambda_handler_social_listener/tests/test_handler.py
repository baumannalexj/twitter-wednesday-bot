from core.date_helper import MINUTES_LAMBDA_TIMEOUT, get_time_min_ago
from datetime import datetime, timezone


def test_get_time_min_ago_returns_past_datetime():
    result = get_time_min_ago(MINUTES_LAMBDA_TIMEOUT)
    now = datetime.now()
    assert result < now
