from typing import TYPE_CHECKING

from constants import CHANNEL_TITLE, ROLE_NAME, STATUS_TO_SYMBOL_MAP
from custom_types import Status
from discord import Colour, Embed
from discord import utils as discord_utils

if TYPE_CHECKING:
    from discord import Guild, Role, TextChannel


def build_channel_title(status: Status) -> str:
    return f"{CHANNEL_TITLE} - {STATUS_TO_SYMBOL_MAP.get(status)}"


async def get_or_create_valheimer_channel(guild: "Guild") -> "TextChannel":
    """
    Returns the valheimer channel for this guild. If none exists, creates it.
    """
    try:
        channel = next((ch for ch in guild.channels if CHANNEL_TITLE in ch.name))
    except StopIteration:
        channel = await guild.create_text_channel(name=CHANNEL_TITLE, position=0)
    return channel


async def get_or_create_valheimer_role(guild: "Guild") -> "Role":
    """
    Returns the valheimer role for this guild. If none exists, creates one.
    """
    if (role := discord_utils.get(guild.roles, name=ROLE_NAME)) is None:
        role = await guild.create_role(
            name=ROLE_NAME,
            colour=Colour.dark_gold(),
            mentionable=True,
            reason="Because",
        )
    return role


async def update_channel_title_with_status(guild: "Guild", status: Status) -> None:
    channel = await get_or_create_valheimer_channel(guild)
    await channel.edit(name=build_channel_title(status))
