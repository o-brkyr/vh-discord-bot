from enum import Enum, auto
from typing import NamedTuple, Optional


class Action(Enum):
    JOIN = auto
    LEAVE = auto
    START = auto


class Message(NamedTuple):
    action: Action
    uid: int
    name: Optional[str]
    time: Optional[int]


class Status(Enum):
    OFFLINE = auto
    ONLINE = auto
    STARTING = auto
    STOPPING = auto
