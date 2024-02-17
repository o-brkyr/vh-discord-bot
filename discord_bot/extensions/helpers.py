from typing import TYPE_CHECKING

from discord.ext import commands

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context


import logging

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(SyncCog.__name__)
    await bot.add_cog(SyncCog(bot))


class SyncCog(WithBotMixin, commands.Cog):
    async def cog_load(self):
        log.info(f"Initialised {self.__cog_name__}")

    @commands.hybrid_command()
    async def sync(self, ctx: "Context"):
        """
        Sync commands with this guild
        """
        self.bot.tree.copy_global_to(guild=ctx.author.guild)
        await self.bot.tree.sync(guild=ctx.author.guild)
        await ctx.send("Synced client command tree with guild")

    @commands.hybrid_command()
    async def reload_cog(self, ctx: "Context", name: str):
        processed_name = f"extensions.{name}"
        await ctx.send(f"Reloading extension '{processed_name}'")
        await self.bot.reload_extension(processed_name)
        await ctx.send(f"Reloaded extension '{processed_name}'.")
