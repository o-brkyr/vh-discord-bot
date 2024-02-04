from enum import Enum, auto


class Status(Enum):
    STOPPED = auto()
    STARTED = auto()
    STARTING = auto()
    STOPPING = auto()
