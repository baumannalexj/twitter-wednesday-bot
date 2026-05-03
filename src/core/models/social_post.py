from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class SocialPost(ABC):
    id: str
    message: str


class TwitterPost(SocialPost):
    id: str
    message: str


@dataclass(frozen=True)
class SocialReply(ABC):
    reply_to_id: str
    message: str


class TwitterReply(SocialReply):
    reply_to_id: str
    message: str
