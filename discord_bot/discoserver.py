import logging
from datetime import datetime
from typing import TYPE_CHECKING

from custom_types import Status
from generated import disco_pb2_grpc
from generated.disco_pb2 import Empty
from settings import SETTINGS
from utils import embeds, guild_utils

if TYPE_CHECKING:
    from discord.ext.commands import Bot
    from generated.disco_pb2 import PlayerRequest, WithTime


log = logging.getLogger(__name__)


def get_time(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp=timestamp).strftime("%a %-d - %H:%M")


class DiscoServer(disco_pb2_grpc.DiscoServicer):
    bot: "Bot"
    status: Status

    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.status = Status.STOPPED

    async def OnPlayerJoin(self, request: "PlayerRequest", context) -> "Empty":
        """
        Called when the server has reported that a player has left.
        """
        channel = await guild_utils.get_or_create_valheimer_channel(
            SETTINGS.target_guild
        )
        await channel.send(
            embed=embeds.player_join(
                request.name, request.extra_name if request.extra_name else None
            )
        )
        return Empty()

    async def OnPlayerLeave(self, request: "PlayerRequest", context) -> "Empty":
        """
        Called when the server has reported that a player has left.
        """
        log.info("Recived 'OnPlayerLeave' RPC call")
        channel = await guild_utils.get_or_create_valheimer_channel(
            SETTINGS.target_guild
        )
        await channel.send(
            embed=embeds.player_leave(
                request.name, request.extra_name if request.extra_name else None
            )
        )
        return Empty()

    async def OnServerSave(self, request: "WithTime", context) -> "Empty":
        """
        Called when the server has reported that the game has saved
        """
        log.info("Recived 'OnServerStart' RPC call")
        return Empty()

    async def OnServerStopped(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has reported that the game is stopped.
        """
        log.info("Recived 'OnServerStopped' RPC call")
        await guild_utils.update_channel_title_with_status(
            self.bot.get_guild(SETTINGS.target_guild), status=Status.STOPPING
        )
        channel = await guild_utils.get_or_create_valheimer_channel(
            self.bot.get_guild(SETTINGS.target_guild)
        )
        await channel.send(embed=embeds.stopped())
        return Empty()

    async def OnServerStart(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has been told to start.
        """
        log.info("Recived 'OnServerStart' RPC call")
        self.status = Status.STARTING

        await guild_utils.update_channel_title_with_status(
            self.bot.get_guild(SETTINGS.target_guild), status=Status.STARTING
        )
        channel = await guild_utils.get_or_create_valheimer_channel(
            self.bot.get_guild(SETTINGS.target_guild)
        )
        await channel.send(embed=embeds.starting())

        return Empty()

    async def OnServerStarted(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has reported that the game is loaded and ready.
        """
        log.info("Recieved 'OnServerStarted' RPC call")
        self.status = Status.STARTED

        await guild_utils.update_channel_title_with_status(
            self.bot.get_guild(SETTINGS.target_guild), status=Status.STARTED
        )
        channel = await guild_utils.get_or_create_valheimer_channel(
            self.bot.get_guild(SETTINGS.target_guild),
        )
        await channel.send(embed=embeds.start())

        return Empty()

    async def OnServerStop(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has been told to stop.
        """
        log.info("Recived 'OnServerStop' RPC call")
        await guild_utils.update_channel_title_with_status(
            self.bot.get_guild(SETTINGS.target_guild), status=Status.STOPPED
        )
        channel = await guild_utils.get_or_create_valheimer_channel(
            self.bot.get_guild(SETTINGS.target_guild)
        )
        await channel.send(embed=embeds.stopping())
        return Empty()
