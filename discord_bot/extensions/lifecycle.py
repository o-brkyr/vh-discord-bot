from typing import TYPE_CHECKING

import grpc
from discord.ext import commands
from generated import val_go_pb2_grpc
from generated.empty_pb2 import Empty
from settings import SETTINGS

from discord_bot.extensions.cog_utils import WithBotMixin, is_guild_owner

if TYPE_CHECKING:
    from discord.ext.commands import Context

import logging

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(ServerLifecycleCommands.__name__)
    await bot.add_cog(ServerLifecycleCommands(bot))


class ServerLifecycleCommands(WithBotMixin, commands.Cog):
    async def cog_load(self):
        log.info(f"Initialised {self.__cog_name__}")

    @commands.hybrid_command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def force_start(self, ctx: "Context"):
        """
        Forces the server to start
        """

        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                stub.ForceStart(Empty())
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return
        await ctx.send("👍 got it fam", ephemeral=True)

    @commands.hybrid_command()
    @commands.check_any(commands.is_owner(), is_guild_owner())
    async def force_stop(self, ctx: "Context"):
        """
        Forces the server to shutdown
        """
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                stub.ForceStop(Empty())
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to shutdown server: {rpc_error}")
            return

        await ctx.send("👍 got it fam", ephemeral=True)
