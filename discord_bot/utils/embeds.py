from datetime import time
from typing import Iterable, Tuple

from discord import Colour, Embed


def register_member(name: str) -> Embed:
    return Embed(
        title="MEMBER REGISTERED",
        colour=Colour.gold(),
        description=f"Succesfully registered '{name}'",
    )


def register_character(character_name: str, member_name: str) -> Embed:
    return Embed(
        title="CHARACTER REGISTERED",
        colour=Colour.gold(),
        description=f"Succesfully registered the character '{character_name}'",
    )


def error(error) -> Embed:
    embed = Embed(
        title="ERROR", colour=Colour.red(), description="Something went wrong"
    ).add_field(name="Description", value=error)
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
