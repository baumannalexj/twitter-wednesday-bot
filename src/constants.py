# UTC+14:00 is earliest timezone on earth, it's wednesday here first

""" #got this media id from the network tab inspecting a specific tweet where I uploaded the image manually:
 https://twitter.com/_isit_wednesday/status/1461140196175630338
 wasn't able to find the
 """
TWITTER_MEDIA_ID_CAPTAIN_ITS_WEDNESDAY = "1461130662002540549"

MESSAGES_ITS_WEDNESDAY = [
    "It is Wednesday.",
    "Today is Wednesday.",
    "It is Wednesday today.",
    "Yes, it is Wednesday.",
    "Wednesday has started.",
    "Welcome to Wednesday.",
]

MESSAGES_NOT_WEDNESDAY = ["Today is not Wednesday.",
                          "Sorry, you'll have to wait.",
                          "Nope.",
                          "Not yet."]

SEARCH_TERMS_WEDNESDAY_HASHTAGS = [
    "#isitwednesday",
    "#isitwednesdayyet",
    "#whensitwednesday",
    "#whenisitwednesday",
    "#whenswednesday",
]

STREAM_RULES = [
    {"value": "#isitwednesday", "tag": "hashtag #isitwednesday"},
    {"value": "#isitwednesdayyet", "tag": "hashtag #isitwednesdayyet"},
    {"value": "#whensitwednesday", "tag": "hashtag #whensitwednesday"},
    {"value": "#whenisitwednesday", "tag": "hashtag #whenisitwednesday"},
    {"value": "#whenswednesday", "tag": "hashtag #whenswednesday"},
]