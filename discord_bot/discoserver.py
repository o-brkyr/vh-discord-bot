import logging
from typing import TYPE_CHECKING, Iterable

import constants
from custom_types import Status
from discord import Colour, Embed
from extensions import channel as extensions_channel
from generated import disco_pb2_grpc
from generated.disco_pb2 import Empty

if TYPE_CHECKING:
    from discord import TextChannel
    from discord.ext.commands import Bot
    from generated.disco_pb2 import PlayerRequest, WithTime


log = logging.getLogger(__name__)


class DiscoServer(disco_pb2_grpc.DiscoServicer):
    """
    A gRPC service that communicates to channels from the go server
    """

    bot: "Bot"
    status: Status

    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.status = Status.STOPPED

    def _get_all_text_channels(self) -> Iterable["TextChannel"]:
        channel_commands: extensions_channel.ChannelCommands = self.bot.get_cog(
            extensions_channel.ChannelCommands.__name__
        )
        if channel_commands is None:
            raise ValueError("Cog not loaded")

        return channel_commands.text_channels

    async def _update_status(self, status: Status) -> None:
        new_title = (
            f"{constants.STATUS_TO_SYMBOL_MAP.get(status)}{constants.CHANNEL_TITLE}"
        )
        for channel in self._get_all_text_channels():
            if channel.name != new_title:
                await channel.edit(name=new_title)

    async def OnPlayerJoin(self, request: "PlayerRequest", context) -> "Empty":
        """
        Called when the server has reported that a player has left.
        """
        for channel in self._get_all_text_channels():
            await channel.send(
                embed=_player_join_embed(
                    request.name, request.extra_name if request.extra_name else None
                )
            )
        return Empty()

    async def OnPlayerLeave(self, request: "PlayerRequest", context) -> "Empty":
        """
        Called when the server has reported that a player has left.
        """
        log.info("Recived 'OnPlayerLeave' RPC call")
        for channel in self._get_all_text_channels():
            await channel.send(
                embed=_player_leave_embed(
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

    async def OnServerStart(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has been told to start.
        """
        log.info("Recived 'OnServerStart' RPC call")

        self._update_status(Status.STARTING)
        for channel in self._get_all_text_channels():
            await channel.send(embed=_starting_embed())

        return Empty()

    async def OnServerStarted(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has reported that the game is loaded and ready.
        """
        log.info("Recieved 'OnServerStarted' RPC call")

        self._update_status(Status.STARTED)
        for channel in self._get_all_text_channels():
            await channel.send(embed=_started_embed())

        return Empty()

    async def OnServerStop(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has been told to stop.
        """
        log.info("Recived 'OnServerStop' RPC call")

        self._update_status(Status.STOPPING)
        for channel in self._get_all_text_channels():
            await channel.send(embed=_stopping_embed())

        return Empty()

    async def OnServerStopped(self, request: "WithTime", context) -> Empty:
        """
        Called when the server has reported that the game is stopped.
        """
        log.info("Recived 'OnServerStopped' RPC call")

        self._update_status(Status.STOPPED)
        for channel in self._get_all_text_channels():
            await channel.send(embed=_stopped_embed())

        return Empty()


def _starting_embed() -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_INBETWEEN} SERVER STARTING",
        colour=Colour.orange(),
        description="Server is starting up. This takes around 5 minutes.",
    )
    return embed


def _started_embed() -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_STARTED} SERVER ONLINE",
        colour=Colour.green(),
        description="Server is now online",
    )
    return embed


def _stopping_embed() -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_INBETWEEN} SERVER SHUTTING DOWN",
        colour=Colour.orange(),
        description="Server is shutting down...",
    )
    return embed


def _stopped_embed() -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_DEAD} SERVER OFFLINE",
        colour=Colour.dark_gray(),
        description="Sever is now offline",
    )
    return embed


def _player_join_embed(name: str, member_name: str | None) -> Embed:
    description = (
        f"{member_name} has joined the server as {name}."
        if member_name
        else f"{name} has joined the server."
    )

    embed = Embed(title="PLAYER JOINED", colour=Colour.green(), description=description)
    return embed


def _player_leave_embed(name: str, member_name: str | None) -> Embed:
    description = (
        f"{member_name} has left the server as {name}."
        if member_name
        else f"{name} has left the server."
    )
    embed = Embed(title="PLAYER LEFT", colour=Colour.purple(), description=description)
    return embed
