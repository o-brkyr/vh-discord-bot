from typing import TYPE_CHECKING
from generated import disco_pb2_grpc
from settings import SETTINGS
from datetime import datetime, date

from generated.disco_pb2 import Empty

import logging


if TYPE_CHECKING:
    from discord.ext.commands import Bot
    from discord.guild import Guild, GuildChannel
    from generated.disco_pb2 import WithTime, WithUserIDAndTime


log = logging.getLogger(__name__)


def get_time(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp=timestamp).strftime("%a %-d - %H:%M")


class DiscoServer(disco_pb2_grpc.DiscoServicer):
    bot: "Bot"

    def __init__(self, bot: "Bot"):
        self.bot = bot

    async def OnPlayerJoin(self, request: "WithUserIDAndTime", context) -> "Empty":
        log.info("Recived 'OnPlayerJoin' RPC call")
        await self.bot.get_channel(SETTINGS.target_channel).send(
            f"Player joined at {get_time(request.timestamp)}"
        )
        return Empty()

    async def OnPlayerLeave(self, request: "WithUserIDAndTime", context) -> "Empty":
        log.info("Recived 'OnPlayerLeave' RPC call")
        await self.bot.get_channel(SETTINGS.target_channel).send(
            f"Player left at {get_time(request.timestamp)}"
        )
        return Empty()

    async def OnServerSave(self, request: "WithTime", context) -> "Empty":
        log.info("Recived 'OnServerStart' RPC call")
        await self.bot.get_channel(SETTINGS.target_channel).send(
            f"Server saved at {get_time(request.timestamp)}"
        )
        return Empty()

    async def OnServerShutdown(self, request: "WithTime", context) -> Empty:
        log.info("Recived 'OnServerStart' RPC call")
        await self.bot.get_channel(SETTINGS.target_channel).send(
            f"Server shutdown at {get_time(request.timestamp)}"
        )
        return Empty()

    async def OnServerStart(self, request: "WithTime", context) -> Empty:
        log.info("Recived 'OnServerStart' RPC call")
        await self.bot.get_channel(SETTINGS.target_channel).send(
            f"Server loaded at {get_time(request.timestamp)}"
        )

        return Empty()
