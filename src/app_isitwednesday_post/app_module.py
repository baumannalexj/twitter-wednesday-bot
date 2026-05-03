import os
from dataclasses import dataclass

from core.services.post_service import PostService


@dataclass(frozen=True)
class AppConfiguration:
    twitter_consumer_key: str
    twitter_consumer_secret: str
    twitter_access_token: str
    twitter_access_token_secret: str


@dataclass(frozen=True)
class AppModule:
    """Testing different import patterns
     Goal is to hide these imports from the app../src files
     """
    config: AppConfiguration

    # SINGLETON PROVIDERS
    def provide_wednesday_service(self) -> PostService:
        from clients.twitter_client import TwitterClient
        from core.services import post_service

        twitter_client = TwitterClient(
            consumer_key=self.config.twitter_consumer_key,
            consumer_secret=self.config.twitter_consumer_secret,
            access_token=self.config.twitter_access_token,
            access_token_secret=self.config.twitter_access_token_secret,
        )

        return post_service.PostService(client=twitter_client)


# CONFIG
config = AppConfiguration(
    twitter_consumer_key=os.environ.get("CONSUMER_KEY"),
    twitter_consumer_secret=os.environ.get("CONSUMER_SECRET"),
    twitter_access_token=os.environ.get("BOT_ACCESS_TOKEN"),
    twitter_access_token_secret=os.environ.get("BOT_ACCESS_TOKEN_SECRET"),
)


app_module = AppModule(config)
