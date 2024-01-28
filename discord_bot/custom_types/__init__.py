from typing import NamedTuple, Optional

from enum import Enum, auto


class Action(Enum):
    JOIN = auto
    LEAVE = auto
    START = auto


class Message(NamedTuple):
    action: Action
    uid: int
    name: Optional[str]
    time: Optional[int]
