from dataclasses import dataclass

from app_config.config import config
from clients.twitter_client import TwitterClient
from core.services.post_service import PostService  # noqa: F401 # see below for dependency injection


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
    """Testing different import and IoC patterns
    Goal is to hide these imports from the app../src files
    """

    post_service: PostService

app_post_module = AppModule(post_service = _provides_post_service())
