from typing import TYPE_CHECKING

from constants import CHANNEL_TITLE, ROLE_NAME
from discord import Colour
from discord.ext import commands

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord import Guild, Role, TextChannel
    from discord.ext.commands import Context

import logging

from utils import guild_utils

log = logging.getLogger(__name__)

COG_NAME = "Channel cog"


async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelCommands(bot))


class ChannelCommands(WithBotMixin, commands.Cog, name=COG_NAME):
    GUILD_ID_TO_CHANNEL_MAP: dict["Guild", "TextChannel"]
    GUILD_ID_TO_GUILD_MAP: dict[int, "Guild"]
    GUILD_ID_TO_ROLE_MAP: dict [int, "Role"]

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.GUILD_ID_TO_CHANNEL_MAP = {}
        self.GUILD_ID_TO_GUILD_MAP = {}
        self.GUILD_ID_TO_ROLE_MAP = {}

    async def _get_or_create_text_channel_for_guild(guild: "Guild") -> "TextChannel":
        try:
            channel = next((ch for ch in guild.channels if CHANNEL_TITLE in ch.name))
        except StopIteration:
            channel = await guild.create_text_channel(name=CHANNEL_TITLE, position=0)
        return channel

    async def _get_or_create_valheimer_role_for_guild(guild: "Guild") -> "Role":
        try:
            role = next((role for role in guild.roles if role.name == ROLE_NAME))
        except StopIteration:
            role = await guild.create_role(
                name=ROLE_NAME,
                colour=Colour.dark_gold(),
                mentionable=True,
                reason="Because",
            )
        return role

    async def get_text_channel_for_guild(self, guild_id: int) -> "TextChannel":
        if (channel := self.GUILD_ID_TO_CHANNEL_MAP.get(guild_id, None)) is None:
            # We haven't saved a guild somehow
            guild = await self.bot.get_guild(guild_id)
            channel = await self._get_or_create_text_channel_for_guild(guild)
            self.GUILD_ID_TO_GUILD_MAP[guild.id] = guild
            self.GUILD_ID_TO_CHANNEL_MAP[guild.id] = channel
        return channel
    
    async def get_role_for_guild(self, guild_id: int) -> "Role":
        if (role := self.GUILD_ID_TO_ROLE_MAP.get(guild_id,None)) is None:
            # We haven't got a role for this bad boy
            guild = await self.bot.get_guild(guild_id)
            role = await self._get_or_create_valheimer_role_for_guild(guild)
            self.GUILD_ID_TO_GUILD_MAP[guild.id] = guild
            self.GUILD_ID_TO_ROLE_MAP[guild.id] = role
        return role

    async def cog_load(self):
        log.info("Loaded cog")
        self.GUILD_ID_TO_GUILD_MAP = {guild.id: guild for guild in self.bot.guilds}
        for guild in self.GUILD_ID_TO_GUILD_MAP.values():
            try:
                channel = next(
                    (ch for ch in guild.channels if CHANNEL_TITLE in ch.name)
                )
            except StopIteration:
                channel = await guild.create_text_channel(
                    name=CHANNEL_TITLE, position=0
                )
            self.GUILD_ID_TO_CHANNEL_MAP[guild.id] = channel
        log.info("Saved guild channels")

    @commands.hybrid_command()
    async def create_valheimer_role(self, ctx: "Context"):
        """
        Create the pingable "Valheimer" role
        """
        # Create a valheimer role in this guild
        await self.get_role_for_guild(ctx.guild.id)
        await ctx.send(content="Added valheimer role!", ephemeral=True)

    @commands.hybrid_command()
    async def create_valheimer_channel(self, ctx: "Context"):
        """
        Create the "Valheimer" channel to send updates to.
        """
        await self.get_text_channel_for_guild(ctx.guild.id)
        await ctx.send(content="Added role", ephemeral=True)

    @commands.hybrid_command()
    async def give_valheimer_role(self,ctx: "Context"):
        """
        Give yourself the Valheimer role.
        """
        role = await self.get_role_for_guild(ctx.guild.id)
        guild: "Guild" = await self.GUILD_ID_TO_GUILD_MAP[ctx.guild.id]
        await ctx.author.add_roles(role.id,"Self-assigned role")
        await ctx.send(content="Assigned role", ephemeral=True)
