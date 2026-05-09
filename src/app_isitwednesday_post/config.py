import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfiguration:
    twitter_consumer_key: str
    twitter_consumer_secret: str
    twitter_access_token: str
    twitter_access_token_secret: str




# CONFIG
config = AppConfiguration(
    twitter_consumer_key=os.environ.get("CONSUMER_KEY"),
    twitter_consumer_secret=os.environ.get("CONSUMER_SECRET"),
    twitter_access_token=os.environ.get("BOT_ACCESS_TOKEN"),
    twitter_access_token_secret=os.environ.get("BOT_ACCESS_TOKEN_SECRET"),
)

