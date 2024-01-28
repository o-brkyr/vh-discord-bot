from dataclasses import dataclass

import tomllib


@dataclass(frozen=True)
class DiscordBotSettings:
    python_to_go_port: int = 0
    go_to_python_port: int = 0
    target_guild: int = 0
    target_channel: int = 0
    bot_token: str = ""


with open("settings.toml", "rb") as f:
    x = tomllib.load(f)
    print(x)

SETTINGS = DiscordBotSettings(**x)
