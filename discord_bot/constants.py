from custom_types import Status

CHANNEL_TITLE = "𝖛𝖆𝖑𝖍𝖊𝖎𝖒"

STATUS_ONLINE = "🟢"
STATUS_OFFLINE = "🔴"
STATUS_INBETWEEN = "🟠"
STATUS_DEAD = "⚫"

ROLE_NAME = "𝔳𝔞𝔩𝔥𝔢𝔦𝔪𝔢𝔯"


STATUS_TO_SYMBOL_MAP: dict[Status, str] = {
    Status.OFFLINE: STATUS_OFFLINE,
    Status.ONLINE: STATUS_ONLINE,
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
