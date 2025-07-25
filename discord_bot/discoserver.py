import logging
from typing import TYPE_CHECKING, Iterable

import constants
from custom_types import Status
from discord import Colour, Embed
from extensions import channel as extensions_channel
from generated import val_py_pb2_grpc
from generated.empty_pb2 import Empty

if TYPE_CHECKING:
    from discord import TextChannel, Role
    from discord.ext.commands import Bot
    from generated.val_py_pb2 import PlayerRequest, StartedRequest


log = logging.getLogger(__name__)


class ValheimPyServer(val_py_pb2_grpc.ValheimPyServicer):
    """
    A gRPC service that communicates to channels from the go server
    """

    bot: "Bot"
    status: Status

    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.status = Status.STOPPED
        log.info(f"Initialised gRPC server")

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

    async def PlayerJoin(self, request: "PlayerRequest", context) -> Empty:
        """
        Called when the server has reported that a player has left.
        """
        for channel in self._get_all_text_channels():
            await channel.send(
                embed=_player_join_embed(
                    request.char_name,
                    request.member_name if request.member_name else None,
                )
            )
        return Empty()

    async def PlayerLeave(self, request: "PlayerRequest", context) -> Empty:
        """
        Called when the server has reported that a player has left.
        """
        log.info("Recived 'OnPlayerLeave' RPC call")
        for channel in self._get_all_text_channels():
            await channel.send(
                embed=_player_leave_embed(
                    request.char_name,
                    request.member_name if request.member_name else None,
                )
            )
        return Empty()

    async def ServerSave(self, request: Empty, context) -> Empty:
        """
        Called when the server has reported that the game has saved
        """
        log.info("Recived 'OnServerSave' RPC call")
        return Empty()

    async def OnStart(self, request: Empty, context) -> Empty:
        """
        Called when the server has been told to start.
        """
        log.info("Recived 'OnServerStart' RPC call")

        # await self._update_status(Status.STARTING)
        for channel in self._get_all_text_channels():
            await channel.send(embed=_starting_embed())

        return Empty()

    async def OnStarted(self, request: "StartedRequest", context) -> Empty:
        """
        Called when the server has reported that the game is loaded and ready.
        """
        log.info("Recieved 'OnServerStarted' RPC call")

        channel_commands: extensions_channel.ChannelCommands = self.bot.get_cog(
            extensions_channel.ChannelCommands.__name__
        )
        if channel_commands is None:
            raise ValueError("Cog not loaded")

        for guild in self.bot.guilds:
            text_channel = await channel_commands.get_text_channel_for_guild(
                guild_id=guild.id
            )
            valheimer_role = await channel_commands.get_role_for_guild(
                guild_id=guild.id
            )
            await text_channel.send(
                embed=_started_embed(
                    valheimer_role=valheimer_role,
                    world=request.world_name,
                    password=request.password,
                    ip=request.ip_address,
                    port=request.port,
                )
            )

        return Empty()

    async def OnStop(self, request: Empty, context) -> Empty:
        """
        Called when the server has been told to stop.
        """
        log.info("Recived 'OnServerStop' RPC call")

        # await self._update_status(Status.STOPPING)
        for channel in self._get_all_text_channels():
            await channel.send(embed=_stopping_embed())

        return Empty()

    async def OnStopped(self, request: Empty, context) -> Empty:
        """
        Called when the server has reported that the game is stopped.
        """
        log.info("Recived 'OnServerStopped' RPC call")

        # await self._update_status(Status.STOPPED)
        for channel in self._get_all_text_channels():
            await channel.send(embed=_stopped_embed())

        return Empty()


def _starting_embed() -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_INBETWEEN} Server starting",
        colour=Colour.orange(),
        description="The server is starting up. This takes around 5 minutes.",
    )
    return embed


def _started_embed(
    ip: str, port: str, password: str, world: str, valheimer_role: "Role"
) -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_STARTED} Server online",
        colour=Colour.green(),
        description=f"{valheimer_role.mention} The server is now online!\n"
        f"Connect to the IP `{ip}:{port}` with the password `{password}`",
    ).add_field(name="World name", value=f"`{world}`")
    return embed


def _stopping_embed() -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_INBETWEEN} Server shutting down",
        colour=Colour.orange(),
        description="The server is shutting down...",
    )
    return embed


def _stopped_embed() -> Embed:
    embed = Embed(
        title=f"{constants.STATUS_DEAD} Server offline",
        colour=Colour.dark_gray(),
        description="Sever is now offline",
    )
    return embed


def _player_join_embed(name: str, member_name: str | None) -> Embed:
    description = (
        f"{name} joined the server! (@{member_name}) ."
        if member_name
        else f"{name} joined the server!"
    )

    embed = Embed(
        title="🏹 Player joined", colour=Colour.green(), description=description
    )
    return embed


def _player_leave_embed(name: str, member_name: str | None) -> Embed:
    description = (
        f"{name} left the server. (@{member_name})."
        if member_name
        else f"{name} left the server."
    )
    embed = Embed(
        title="🏹 Player left", colour=Colour.purple(), description=description
    )
    return embed
