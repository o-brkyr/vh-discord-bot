from datetime import time
from typing import TYPE_CHECKING, Literal, List, Tuple

import grpc
from discord.ext import commands
from generated import disco_pb2_grpc
from generated.disco_pb2 import ScheduleRequest, ScheduleMessage
from settings import SETTINGS
from utils import embeds

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context

import logging

log = logging.getLogger(__name__)

COG_NAME = "Schedule cog"


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(ScheduleCommands(bot))


WEEKDAY_AS_INT_MAP: dict[str, int] = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


class ScheduleCommands(WithBotMixin, commands.Cog, name=COG_NAME):
    def cog_load(self):
        log.info("Loaded cog")

    @commands.hybrid_command()
    async def get_schedule_for_day(
        self,
        ctx: "Context",
        weekday: Literal[
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ],
    ):
        weekday_as_int = WEEKDAY_AS_INT_MAP.get(weekday, 0)
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                session_times: List[Tuple[time,time]] = []
                for resp in stub.GetDaySchedule(
                    ScheduleRequest(weekday=weekday_as_int)
                ):
                    resp: ScheduleMessage
                    session_times.append((time.fromisoformat(resp.start_time),time.fromisoformat(resp.end_time)))
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        embed = embeds.day_schedule(weekday,session_times)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def set_schedule_for_day(
        self,
        ctx: "Context",
        weekday: Literal[
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ],
        start_time: str,
        end_time: str
    ):
        weekday_as_int = WEEKDAY_AS_INT_MAP.get(weekday, 0)

        start_time = start_time.strip()
        end_time = end_time.strip()

        try:
            start_time_time = time.fromisoformat(start_time)
        except ValueError:
            await ctx.send(f"Invalid start time: {start_time}. Try the following format: '16:30'")
            return
        
        try:
            end_time_time = time.fromisoformat(end_time)
        except ValueError:
            await ctx.send(f"Invalid end time: {end_time}. Try the following format: '16:30'")
            return


        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                response: ScheduleMessage = stub.SetDaySchedule(
                    ScheduleMessage(
                        weekday=weekday_as_int,
                        start_time=start_time,
                        end_time=end_time
                    )
                )
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        embed = embeds.day_schedule(weekday,[(start_time_time,end_time_time)])
        await ctx.send(embed=embed)