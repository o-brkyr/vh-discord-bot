from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord.ext.commands import Bot

import logging

log = logging.getLogger(__name__)


class WithBotMixin:
    bot: "Bot"

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
