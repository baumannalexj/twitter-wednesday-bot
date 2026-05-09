from dataclasses import dataclass, field

from app_isitwednesday_post.config import AppConfiguration, config
from app_isitwednesday_post.lambda_resource import LambdaResource
from clients.twitter_client import TwitterClient
from core import CoreModule
from core.services.post_service import PostService  # noqa: F401 # see below for dependency injection


def _provides_core_module(self) -> CoreModule:
    twitter_client = TwitterClient(
        consumer_key=self.config.twitter_consumer_key,
        consumer_secret=self.config.twitter_consumer_secret,
        access_token=self.config.twitter_access_token,
        access_token_secret=self.config.twitter_access_token_secret,

    )

    core_module = CoreModule(post_service=PostService(_client=twitter_client))
    return core_module

class AppModule:
    """Testing different import patterns
    Goal is to hide these imports from the app../src files
    """

    config: AppConfiguration
    lambda_resource: LambdaResource

    def __init__(self, config: AppConfiguration) -> None:
        self.config = config

        core_module = _provides_core_module(self)
        self.lambda_resource = LambdaResource(post_service=core_module.post_service)





app_reply_module = AppModule(config=config)
