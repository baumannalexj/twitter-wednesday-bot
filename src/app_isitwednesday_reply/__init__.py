import logging
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
)


def _wireup() -> tuple:
    """testing different import patterns, goal is to hide these imports from the app../src files"""

    from clients.twitter_client import TwitterClient
    from core.services import wednesday_service

    twitter_client = TwitterClient(
        consumer_key=os.environ.get("CONSUMER_KEY"),
        consumer_secret=os.environ.get("CONSUMER_SECRET"),
        access_token=os.environ.get("BOT_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("BOT_ACCESS_TOKEN_SECRET"),
    )

    wednesday_service = wednesday_service.WednesdayService(client=twitter_client)

    example_noop = lambda: print(1)

    return (wednesday_service, example_noop)


app = _wireup()
