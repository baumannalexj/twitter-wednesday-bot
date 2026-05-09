from dataclasses import dataclass, field

from app_isitwednesday_post.config import AppConfiguration, config
from app_isitwednesday_post.lambda_resource import LambdaResource
from clients.twitter_client import TwitterClient
from core import CoreModule
from core.services.post_service import PostService  # noqa: F401 # see below for dependency injection


@dataclass(frozen=True)
class AppModule:
    """Testing different import patterns
    Goal is to hide these imports from the app../src files
    """

    config: AppConfiguration
    lambda_resource: LambdaResource = field(init=False)

    def __post_init__(self):
        core_module = self.provides_core_module()

        object.__setattr__(self, "lambda_resource",
                           LambdaResource(post_service=core_module.post_service)
                           )

    def provides_core_module(self) -> CoreModule:
        twitter_client = TwitterClient(
            consumer_key=self.config.twitter_consumer_key,
            consumer_secret=self.config.twitter_consumer_secret,
            access_token=self.config.twitter_access_token,
            access_token_secret=self.config.twitter_access_token_secret,

        )

        core_module = CoreModule(post_service=PostService(_client=twitter_client))
        return core_module


app_post_module = AppModule(config=config)
