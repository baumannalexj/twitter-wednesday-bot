from dataclasses import dataclass

from app_config.config import config
from clients.twitter_client import TwitterClient
from core.services.post_service import PostService


def _provides_post_service() -> PostService:
    twitter_client = TwitterClient(
        consumer_key=config.twitter_consumer_key,
        consumer_secret=config.twitter_consumer_secret,
        access_token=config.twitter_access_token,
        access_token_secret=config.twitter_access_token_secret,
    )
    return PostService(_client=twitter_client)


@dataclass(frozen=True)
class AppModule:
    post_service: PostService


app_reply_module = AppModule(post_service=_provides_post_service())
