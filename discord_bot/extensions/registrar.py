from typing import TYPE_CHECKING

import grpc
from discord.ext import commands
from generated import val_go_pb2_grpc
from generated.empty_pb2 import Empty
from generated.val_go_pb2 import (
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

COG_NAME = "RegistrationCog"


async def setup(bot: commands.Bot):
    await bot.remove_cog(RegistrationCog.__name__)
    await bot.add_cog(RegistrationCog(bot))


class RegistrationCog(WithBotMixin, commands.Cog):
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
            if response.status == RegistrationStatus.REGISTRATIONSTATUS_REGISTERED:
                await ctx.send(
                    embed=embeds.register_character(response.characters[0].char_name),
                    ephemeral=True,
                )
            else:
                await ctx.send(embed=embeds.error(response.message), ephemeral=True)

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
            if response.status == RegistrationStatus.REGISTRATIONSTATUS_REGISTERED:
                await ctx.send(embed=embeds.register_member(response.message))
            else:
                await ctx.send(embed=embeds.error(response.message), ephemeral=True)
