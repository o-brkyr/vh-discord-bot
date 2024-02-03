import logging
from typing import TYPE_CHECKING

from discord.ext import commands

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context


log = logging.getLogger(__name__)

COG_NAME = "ExtensionReloader"


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(ExtensionReloader(bot))


class ExtensionReloader(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        log.info("Loaded cog")

    @commands.hybrid_command()
    async def reload_cog(self, ctx: "Context", name: str):
        processed_name = f"extensions.{name}"
        await ctx.send(f"Reloading extension '{processed_name}'")
        await self.bot.reload_extension(processed_name)
        await ctx.send(f"Reloaded extension '{processed_name}'.")
