from typing import TYPE_CHECKING

from discord.ext import commands
from extensions.utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context

COG_NAME = "ExtensionReloader"

import logging

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(ExtensionReloader(bot))


class ExtensionReloader(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        print(f"Loaded <{COG_NAME}>")

    @commands.hybrid_command()
    async def reload_cog(self, ctx: "Context", name: str):
        await ctx.send(f"Reloading extension '{name}'")
        await self.bot.reload_extension(name)
        await ctx.send(f"Reloaded extension '{name}'.")
