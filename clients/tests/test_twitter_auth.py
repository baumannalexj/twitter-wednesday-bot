from clients.twitter import auth


def test_auth_module_exists():
    assert hasattr(auth, 'get_twitter_oauth1_client')
    assert hasattr(auth, 'get_bearer_auth_header')
