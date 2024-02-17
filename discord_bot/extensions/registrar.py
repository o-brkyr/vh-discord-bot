from typing import TYPE_CHECKING

import grpc
from discord.ext import commands
from generated import disco_pb2_grpc
from generated.disco_pb2 import RegisterRequest, Result, ResultResponse
from settings import SETTINGS
from utils import embeds

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context
    from generated.disco_pb2 import ResultResponse

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
                stub = disco_pb2_grpc.DiscoStub(channel)
                response: ResultResponse = stub.DoRegisterCharacter(
                    RegisterRequest(name=character_name, member_id=ctx.author.id)
                )
                if response.result == Result.RESULT_OK:
                    await ctx.send(
                        embed=embeds.register_character(
                            response.message, ctx.author.name
                        )
                    )
                else:
                    await ctx.send(embed=embeds.error(response.message), ephemeral=True)
        except grpc.RpcError as rpc_error:
            await ctx.send(embed=embeds.error(rpc_error), ephemeral=True)

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
                stub = disco_pb2_grpc.DiscoStub(channel)
                response: ResultResponse = stub.DoRegisterMember(
                    RegisterRequest(
                        name=ctx.author.global_name, member_id=ctx.author.id
                    )
                )
                if response.result == Result.RESULT_OK:
                    await ctx.send(embed=embeds.register_member(response.message))
                else:
                    await ctx.send(embed=embeds.error(response.message), ephemeral=True)
        except grpc.RpcError as rpc_error:
            await ctx.send(embed=embeds.error(rpc_error), ephemeral=True)
