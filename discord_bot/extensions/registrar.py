from datetime import datetime
from typing import TYPE_CHECKING

import grpc
from discord.ext import commands
from extensions.utils import WithBotMixin
from generated import disco_pb2_grpc
from generated.disco_pb2 import WithTime
from settings import SETTINGS

if TYPE_CHECKING:
    from discord.ext.commands import Context
    from generated.disco_pb2 import ResultResponse

import logging

log = logging.getLogger(__name__)

COG_NAME = "Register cog"


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(RegistrationCommands(bot))


class RegistrationCommands(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        log.info("Loaded Registration cog")

    @commands.hybrid_command()
    async def register_character(self, ctx: "Context", character_name: str) -> None:
        """
        Register a character
        
        A character being the name of an individual a character a member may play as.
        """
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                response: ResultResponse = stub.(
                    WithTime(timestamp=int(datetime.now().timestamp()))
                )

