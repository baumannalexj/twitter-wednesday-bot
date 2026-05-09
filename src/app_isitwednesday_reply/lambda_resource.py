import datetime
from dataclasses import dataclass

from core.services.post_service import PostService


@dataclass(frozen=True)
class LambdaResource:
    post_service: PostService

    def lambda_handler(self, event, context, start_time_iso=datetime.datetime) -> None:
        self.post_service.reply_to_recent_wednesday_tweets(self, start_time_iso=start_time_iso)
        return None
