from custom_types import Status

CHANNEL_TITLE = "𝖛𝖆𝖑𝖍𝖊𝖎𝖒"

STATUS_STARTED = "🟢"
STATUS_STOPPED = "🔴"
STATUS_INBETWEEN = "🟠"
STATUS_DEAD = "⚫"

ROLE_NAME = "𝔳𝔞𝔩𝔥𝔢𝔦𝔪𝔢𝔯"


STATUS_TO_SYMBOL_MAP: dict[Status, str] = {
    Status.STOPPED: STATUS_STOPPED,
    Status.STARTED: STATUS_STARTED,
    Status.STARTING: STATUS_INBETWEEN,
    Status.STOPPING: STATUS_INBETWEEN,
}


WEEKDAY_AS_INT_MAP: dict[str, int] = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}
