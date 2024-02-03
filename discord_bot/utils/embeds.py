from datetime import time
from typing import Iterable, Tuple

from discord import Colour, Embed


def player_join(name: str, member_name: str | None) -> Embed:
    description = (
        f"{member_name} has joined the server as {name}."
        if member_name
        else f"{name} has joined the server."
    )

    embed = Embed(title="PLAYER JOINED", colour=Colour.green(), description=description)
    return embed


def player_leave(name: str, member_name: str | None) -> Embed:
    description = (
        f"{member_name} has left the server as {name}."
        if member_name
        else f"{name} has left the server."
    )
    embed = Embed(title="PLAYER LEFT", colour=Colour.purple(), description=description)
    return embed


def error(error) -> Embed:
    embed = Embed(
        title="ERROR", colour=Colour.red(), description="Something went wrong"
    ).add_field("Description", error)
    return embed


def start() -> Embed:
    embed = Embed(
        title="SERVER ONLINE", colour=Colour.green(), description="Server is now online"
    )
    return embed


def stopped() -> Embed:
    embed = Embed(
        title="SERVER OFFLINE",
        colour=Colour.dark_grey(),
        description="Sever is now offline",
    )
    return embed


def stopping() -> Embed:
    embed = Embed(
        title="SERVER SHUTTING DOWN",
        colour=Colour.orange(),
        description="Server is shutting down...",
    )
    return embed


def starting() -> Embed:
    embed = Embed(
        title="SERVER STARTING",
        colour=Colour.orange(),
        description="Server is starting up...",
    )
    return embed


def day_schedule(weekday: str, sessions: Iterable[Tuple[time, time]]) -> Embed:
    embed = Embed(
        title=f"Schedule for {weekday}",
        colour=Colour.blue(),
    )

    if len(sessions) == 0:
        embed.description = "There are no sessions scheduled for this day."
        return embed

    for n, time_pair in enumerate(sessions):
        start_time, end_time = time_pair
        start_time: time
        end_time: time
        embed.add_field(
            name=f"Session {n+1}",
            value=f'From {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}',
        )
    return embed


def player_list() -> Embed:
    embed = Embed(
        title="Player list",
        colour=Colour.blue(),
    )
    return embed
