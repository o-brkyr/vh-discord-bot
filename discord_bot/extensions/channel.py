from typing import TYPE_CHECKING

from discord.ext import commands
from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context

import logging

from utils import guild_utils

log = logging.getLogger(__name__)

COG_NAME = "Channel cog"


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(ChannelCommands(bot))


class ChannelCommands(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        log.info("Loaded cog")

    @commands.hybrid_command()
    async def add_valheimer_role(self, ctx: "Context"):
        await guild_utils.get_or_create_valheimer_role(ctx.guild)
        await ctx.send(content="Added role", ephemeral=True)

    @commands.hybrid_command()
    async def add_valheimer_channel(self, ctx: "Context"):
        await guild_utils.get_or_create_valheimer_channel(ctx.guild)
        await ctx.send(content="Added role", ephemeral=True)
