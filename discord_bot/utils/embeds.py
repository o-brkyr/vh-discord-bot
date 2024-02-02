from discord import Embed, Colour
from datetime import date, time
import calendar

from typing import Iterable, Tuple


def player_join(name: str) -> Embed:
    embed = Embed(
        title="PLAYER JOINED",
        colour=Colour.green(),
        description=f"{name} has joined the server.",
    )
    return embed


def player_leave(name: str) -> Embed:
    embed = Embed(
        title="PLAYER LEFT",
        colour=Colour.purple(),
        description=f"{name} left the server because they suck",
    )
    return embed


def error(error) -> Embed:
    embed = Embed(
        title="ERROR", colour=Colour.red(), description="Something went wrong"
    ).add_field("Description", error)
    return embed


def start() -> Embed:
    embed = Embed(
        title="SERVER ONLINE", colour=Colour.green(), description="Server is online"
    )
    return embed


def shutdown() -> Embed:
    embed = Embed(
        title="SERVER OFFLINE",
        colour=Colour.dark_grey(),
        description="Sever is now offline",
    )
    return embed

def day_schedule(weekday: str,sessions: Iterable[Tuple[time,time]]) -> Embed:
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
            name=f'Session {n+1}',
            value=f'From {start_time.strftime('%H:%M:%S')} to {end_time.strftime('%H:%M:%S')}'
        )
    return embed