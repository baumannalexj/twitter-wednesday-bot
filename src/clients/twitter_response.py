import enum

from pydantic import BaseModel


class TweetReplySettings(enum.StrEnum):
    """Who can reply to the post
    "everyone" is the default behavior if the parameter is omitted
    """

    EVERYONE = "everyone"
    FOLLOWERS = "following"
    MENTIONED_USERS = "mentionedUsers"
    SUBSCRIBERS = "subscribers"
    VERIFIED = "verified"


class TweetResponse(BaseModel):
    id: str
    text: str
    possibly_sensitive: bool = False
    reply_settings: TweetReplySettings = TweetReplySettings.EVERYONE # api default, including when omitted in response

    def is_eligible(self) -> bool:
        return self.reply_settings == TweetReplySettings.EVERYONE and not self.possibly_sensitive
