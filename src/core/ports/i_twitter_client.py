import datetime
from abc import ABC, abstractmethod

from core.models.social_post import SocialPost, SocialReply


class ITwitterClient(ABC):
    @abstractmethod
    def find_recent_hashtags_posts(
        self,
        hashtags_to_search: list[str],
        start_time_iso: datetime.datetime,
        since_id: str | None = None,
        max_results: int | None = None,
    ) -> list[SocialPost]:
        """Search for recent posts based on a query."""
        pass

    @abstractmethod
    def post_tweet(self, text: str, media_ids: list[str] | None = None) -> SocialPost:
        """Post a new message or reply."""
        pass

    @abstractmethod
    def reply_to_tweet(self, post_reply: SocialReply) -> SocialPost:
        """Post a new message or reply."""
        pass
