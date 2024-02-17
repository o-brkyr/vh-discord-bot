from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord.ext.commands import Bot


class WithBotMixin:
    bot: "Bot"

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
