response_post_reply = {
    "data": {
        "id": "1445827346513514500",
        "text": "This is a reply to the previous tweet.",
        "edit_history_tweet_ids": ["1445827346513514501"],
        "an_extra_field": ["an extra value"],
    }
}

response_post_tweet = {
    "data": {
        "id": "1445827346513514498",
        "text": "Hello world! This is a test tweet.",
        "edit_history_tweet_ids": ["1445827346513514498"],
        "an_extra_field": ["an extra value"],
    }
}


response_twitter_search = {
    "data": [
        {
            "text": "#isitwednesday eligible with reply_settings=everyone",
            "id": "1461374568799604741",
            "possibly_sensitive": False,
            "reply_settings": "everyone",
            "created_at": "2021-11-18T16:43:42.000Z",
            "an_extra_field": ["an extra value"],
        },
        {
            "text": "#isitwednesday this is eligible without the reply_settings",
            "id": "1461374568799604742",
            "possibly_sensitive": False,
            "an_extra_field": ["an extra value"],
            "created_at": "2021-11-18T18:43:42.000Z",
        },
        {
            "text": "long week #isitwednesdayyet",
            "id": "1461366708124327950",
            "possibly_sensitive": True,
            "an_extra_field": ["an extra value"],
            "reply_settings": "everyone",
            "created_at": "2021-11-18T16:12:28.000Z",
        },
        {
            "an_extra_field": ["an extra value"],
            "id": "1346889436626259969",
            "edit_history_tweet_ids": ["1346889436626259969"],
            "text": "This tweet has restricted replies.",
            "possibly_sensitive": True,
            "reply_settings": "following",
        },
    ],
    "meta": {"newest_id": "1461374568799604741", "oldest_id": "1461366708124327950", "result_count": 3},
}
