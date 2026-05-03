from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class SocialPostModel(ABC):
    id: str
    message: str


class TwitterPostModel(SocialPostModel):
    id: str
    message: str


@dataclass(frozen=True)
class SocialReply(ABC):
    reply_to_id: str
    message: str


class TwitterReplyModel(SocialReply):
    reply_to_id: str
    message: str
