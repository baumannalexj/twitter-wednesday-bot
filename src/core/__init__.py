"""Composition root: reads config, builds clients, wires them into services."""

import logging
import os

from clients.twitter import TwitterClient
from core.services import WednesdayService

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.root.setLevel(LOG_LEVEL)

twitter_client = TwitterClient(
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    bearer_token=os.environ.get("BEARER_TOKEN"),
    access_token=os.environ.get("BOT_ACCESS_TOKEN"),
    access_token_secret=os.environ.get("BOT_ACCESS_TOKEN_SECRET"),
)

wednesday_service = WednesdayService(twitter_client=twitter_client)
