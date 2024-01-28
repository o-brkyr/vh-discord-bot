from typing import TYPE_CHECKING

from discord.ext import commands
from extensions.utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context


COG_NAME = "SyncFunc"

import logging

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(SyncFunc(bot))


class SyncFunc(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        print("Loaded Sync Cog")

    @commands.hybrid_command()
    async def force_sync(self, ctx: "Context"):
        print("Attempting to sync")
        print(f"{ctx.interaction=}")
        print(f"{ctx.author=}, \n{ctx.author.guild=}, \n{ctx.author.guild.id=}")
        self.bot.tree.copy_global_to(guild=ctx.author.guild)
        await self.bot.tree.sync(guild=ctx.author.guild)
        await ctx.send("Syncing client command tree with guild")
