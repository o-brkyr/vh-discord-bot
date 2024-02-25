from typing import TYPE_CHECKING, Iterable

import grpc
from discord import Colour, Embed
from discord.ext import commands
from generated import val_go_pb2_grpc
from generated.empty_pb2 import Empty
from generated.val_go_pb2 import (
    PlayerData,
    QueryPlayersResponse,
    RegisterMemberResponse,
    RegisterRequest,
    RegisterResponse,
    RegistrationStatus,
)
from settings import SETTINGS
from utils import embeds

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context

import logging

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(PlayerCog.__name__)
    await bot.add_cog(PlayerCog(bot))


class PlayerCog(WithBotMixin, commands.Cog):
    async def cog_load(self):
        log.info(f"Initialised {self.__cog_name__}")

    @commands.hybrid_command()
    async def register_character(self, ctx: "Context", character_name: str) -> None:
        """
        Register a character

        A character being the name of an individual a character a member may play as.
        """
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                response: RegisterResponse = stub.RegisterCharacter(
                    RegisterRequest(char_name=character_name, snowflake=ctx.author.id)
                )
        except grpc.RpcError as rpc_error:
            await ctx.send(embed=embeds.error(rpc_error), ephemeral=True)
        else:
            if response.status != RegistrationStatus.REGISTRATIONSTATUS_REGISTERED:
                await ctx.send(
                    embed=_register_character(
                        character_name=character_name,
                        member_name=ctx.author.global_name,
                        success=False,
                    ),
                    ephemeral=True,
                )
            else:
                await ctx.send(
                    embed=_register_character(
                        character_name=character_name,
                        member_name=ctx.author.global_name,
                        success=True,
                    )
                )

    @commands.hybrid_command()
    async def register_member(
        self,
        ctx: "Context",
    ) -> None:
        """
        Register a member

        A member is an alias for a discord user.
        """
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                response: RegisterMemberResponse = stub.RegisterMember(
                    RegisterRequest(
                        char_name=ctx.author.global_name, snowflake=ctx.author.id
                    )
                )
        except grpc.RpcError as rpc_error:
            await ctx.send(embed=embeds.error(rpc_error), ephemeral=True)
        else:
            if response.status != RegistrationStatus.REGISTRATIONSTATUS_REGISTERED:
                await ctx.send(
                    embed=_register_member(ctx.author.global_name, False),
                    ephemeral=True,
                )
            else:
                await ctx.send(embed=_register_member(ctx.author.global_name))

    @commands.hybrid_command()
    async def player_list(
        self,
        ctx: "Context",
    ) -> None:
        """
        Get players in the server
        """
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                response: QueryPlayersResponse = stub.QueryPlayers(Empty())
                if not response.player_list:
                    await ctx.send(embed=_no_players(), ephemeral=True)
                    return
                await ctx.send(embed=_player_list(response.player_list))
        except grpc.RpcError as rpc_error:
            await ctx.send(embed=_error(rpc_error), ephemeral=True)


def _register_member(member_name: str, success: bool = True) -> Embed:
    if success:
        return Embed(
            title="✅ Registered member",
            colour=Colour.green(),
            description=f"Succesfully registered {member_name}!",
        )
    return Embed(
        title="⚠️ Could not register member",
        colour=Colour.yellow(),
        description=f"You are already registered.",
    )


def _register_character(
    character_name: str, member_name: str, success: bool = True
) -> Embed:
    if success:
        return Embed(
            title="✅ Registered character",
            colour=Colour.green(),
            description=f"{member_name} registered the character `{character_name}`!",
        )
    return Embed(
        title="⚠️ Could not register character",
        colour=Colour.yellow(),
        description=f"Could not register '{character_name}' - that character is already registered.",
    )


def _offline() -> Embed:
    return Embed(
        title="🏹 Player list",
        colour=Colour.dark_gray(),
        description="Server is currently offline",
    )


def _no_players() -> Embed:
    return Embed(
        title="🏹 Player list",
        colour=Colour.dark_gray(),
        description="Server is currently empty",
    )


def _error(err) -> Embed:
    return Embed(
        title="🚨 Error",
        colour=Colour.red(),
        description=f"Encountered an error!\n{err}",
    )


def _player_list(player_datas: Iterable[PlayerData]) -> Embed:
    e = Embed(
        title="🏹 Player list", colour=Colour.blue(), description="Current player list:"
    )
    character_names, member_names, play_time = [], [], []
    for player in player_datas:
        character_names.append(player.char_name)
        member_names.append(player.member_name or "")
        play_time.append(str(player.playtime_s) or "0")
    e.add_field(name="Characters", value="\n".join(character_names))
    e.add_field(name="Member", value="\n".join(member_names))
    e.add_field(name="Playtime", value="\n".join(play_time))

    return e
