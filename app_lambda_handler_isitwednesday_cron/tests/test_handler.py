

def test_pick_wednesday_message_returns_string():
    msg = pick_wednesday_message()
    assert isinstance(msg, str)
    assert len(msg) > 0


def test_pick_non_wednesday_message_returns_string():
    msg = pick_non_wednesday_message()
    assert isinstance(msg, str)
    assert len(msg) > 0
