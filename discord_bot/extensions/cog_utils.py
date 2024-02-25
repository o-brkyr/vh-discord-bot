from typing import TYPE_CHECKING
from discord.ext import commands

if TYPE_CHECKING:
    from discord.ext.commands import Bot


class WithBotMixin:
    bot: "Bot"

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

    return commands.check(predicate)
