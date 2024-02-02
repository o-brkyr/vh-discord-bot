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
    Status.STARTING: f"{STATUS_OFFLINE} -> {STATUS_ONLINE}",
    Status.STOPPING: f"{STATUS_ONLINE} -> {STATUS_OFFLINE}",
}
