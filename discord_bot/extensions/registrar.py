from typing import TYPE_CHECKING

import grpc
from discord.ext import commands
from generated import disco_pb2_grpc
from generated.disco_pb2 import RegisterRequest, ResultResponse, Result
from settings import SETTINGS

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context
    from generated.disco_pb2 import ResultResponse

import logging

log = logging.getLogger(__name__)

COG_NAME = "Register cog"


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(RegistrationCommands(bot))


class RegistrationCommands(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        log.info("Loaded cog")

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
                    await ctx.send(response.message)
                else:
                    await ctx.send(f"Failed to register character: {response.message}")
        except grpc.RpcError as rpc_error:
            await ctx.send(f"RPC error occured: {rpc_error}")

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
                    await ctx.send(response.message)
                else:
                    await ctx.send(f"Failed to register member: {response.message}")
        except grpc.RpcError as rpc_error:
            await ctx.send(f"RPC error occurred: {rpc_error}")
