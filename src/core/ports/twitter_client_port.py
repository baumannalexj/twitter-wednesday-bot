import datetime
from abc import ABC, abstractmethod

from core.models.social_post import SocialPostModel, SocialReply


class ITwitterClient(ABC):
    @abstractmethod
    def find_recent_hashtags_posts(
        self,
        hashtags_to_search: list[str],
        start_time_iso: datetime.datetime,
        since_id: str | None = None,
        max_results: int | None = None,
    ) -> list[SocialPostModel]:
        """Search for recent posts based on a query."""
        pass

    @abstractmethod
    def post_tweet(self, message_string: str, media_ids: list[str] | None = None) -> SocialPostModel:
        """Post a new message or reply."""
        pass

    @abstractmethod
    def reply_to_tweet(self, post_reply: SocialReply) -> SocialPostModel:
        """Post a new message or reply."""
        pass
