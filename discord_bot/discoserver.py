from typing import TYPE_CHECKING
from generated import disco_pb2_grpc
from settings import SETTINGS
from datetime import datetime

from generated.disco_pb2 import Empty
from custom_types import Status
import logging
from utils import guild_utils, embeds


if TYPE_CHECKING:
    from discord.ext.commands import Bot
    from generated.disco_pb2 import WithTime, WithUserIDAndTime


log = logging.getLogger(__name__)


def get_time(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp=timestamp).strftime("%a %-d - %H:%M")


class DiscoServer(disco_pb2_grpc.DiscoServicer):
    bot: "Bot"
    status: Status

    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.status = Status.OFFLINE

    async def OnPlayerJoin(self, request: "WithUserIDAndTime", context) -> "Empty":
        log.info("Recived 'OnPlayerJoin' RPC call")
        await guild_utils.get_or_create_valheimer_channel(SETTINGS.target_guild).send(
            embed=embeds.player_join("player?")
        )
        return Empty()

    async def OnPlayerLeave(self, request: "WithUserIDAndTime", context) -> "Empty":
        log.info("Recived 'OnPlayerLeave' RPC call")
        await guild_utils.get_or_create_valheimer_channel(SETTINGS.target_guild).send(
            embed=embeds.player_leave("player?")
        )
        return Empty()

    async def OnServerSave(self, request: "WithTime", context) -> "Empty":
        log.info("Recived 'OnServerStart' RPC call")

        return Empty()

    async def OnServerShutdown(self, request: "WithTime", context) -> Empty:
        log.info("Recived 'OnServerShutdown' RPC call")
        await guild_utils.update_channel_title_with_status(
            self.bot.get_guild(SETTINGS.target_guild), status=Status.STOPPING
        )
        await guild_utils.get_or_create_valheimer_channel(SETTINGS.target_guild).send(
            embed=embeds.shutdown()
        )
        return Empty()

    async def OnServerStart(self, request: "WithTime", context) -> Empty:
        log.info("Recived 'OnServerStart' RPC call")
        self.status = Status.ONLINE

        await guild_utils.update_channel_title_with_status(
            self.bot.get_guild(SETTINGS.target_guild), status=Status.ONLINE
        )
        await guild_utils.get_or_create_valheimer_channel(SETTINGS.target_guild).send(
            embed=embeds.start()
        )

        return Empty()
