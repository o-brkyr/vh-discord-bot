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

COG_NAME = "ServerLifecycleCommands"


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(ServerLifecycleCommands(bot))


class ServerLifecycleCommands(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        log.info("Loaded cog")

    @commands.hybrid_command()
    async def force_start_servster(self, ctx: "Context"):
        """
        Forces the server to start
        """
        # if not is_admin(ctx):
        #     await ctx.send("You don't have permission to do that.")
        #     return

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

        await ctx.send(f"Recieved start response: {response.code}")

    @commands.hybrid_command()
    async def force_shutdown_server(self, ctx: "Context"):
        """
        Forces the server to shutdown
        """
        # if not is_admin(ctx):
        #     await ctx.send("You don't have permission to do that.")
        #     return

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

        await ctx.send(f"Recieved shutdown response: {response.code}")
