from typing import TYPE_CHECKING

from discord.ext import commands

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context


import logging

COG_NAME = "SyncCog"

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(SyncCog(bot))


class SyncCog(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        log.info("Loaded cog")

    @commands.hybrid_command()
    async def sync(self, ctx: "Context"):
        """
        Sync commands with this guild
        """
        self.bot.tree.copy_global_to(guild=ctx.author.guild)
        await self.bot.tree.sync(guild=ctx.author.guild)
        await ctx.send("Synced client command tree with guild")
