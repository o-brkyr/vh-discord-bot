from datetime import datetime
from typing import TYPE_CHECKING

import grpc
from discord.ext import commands
from generated import disco_pb2_grpc
from generated.disco_pb2 import WithTime
from settings import SETTINGS

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context
    from generated.disco_pb2 import ResultResponse

import logging

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(ServerLifecycleCommands.__name__)
    await bot.add_cog(ServerLifecycleCommands(bot))


class ServerLifecycleCommands(WithBotMixin, commands.Cog):
    async def cog_load(self):
        log.info(f"Initialised {self.__cog_name__}")

    @commands.hybrid_command()
    async def force_start(self, ctx: "Context"):
        """
        Forces the server to start
        """

        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                response: ResultResponse = stub.DoServerStart(
                    WithTime(timestamp=int(datetime.now().timestamp()))
                )
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        if response.code != 200:
            await ctx.send(
                f"Error recieved - code {response.code}, message: '{response.message}'"
            )
        else:
            await ctx.send("👍 got it fam", ephemeral=True)

    @commands.hybrid_command()
    async def force_stop(self, ctx: "Context"):
        """
        Forces the server to shutdown
        """
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                response: ResultResponse = stub.DoServerShutdown(
                    WithTime(timestamp=int(datetime.now().timestamp()))
                )
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to shutdown server: {rpc_error}")
            return

        if response.code != 200:
            await ctx.send(
                f"Error recieved - code {response.code}, message: '{response.message}'"
            )
        else:
            await ctx.send("👍 got it fam", ephemeral=True)
