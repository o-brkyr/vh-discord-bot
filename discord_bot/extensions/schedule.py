from datetime import time
from typing import TYPE_CHECKING, List, Literal, Tuple

import grpc
from discord.ext import commands
from generated import disco_pb2_grpc
from generated.disco_pb2 import ScheduleMessage, ScheduleRequest
from settings import SETTINGS
from utils import embeds, time_utils

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context

import logging

log = logging.getLogger(__name__)

COG_NAME = "Schedule cog"


async def setup(bot: commands.Bot):
    await bot.remove_cog(COG_NAME)
    await bot.add_cog(ScheduleCog(bot))


WEEKDAY_AS_INT_MAP: dict[str, int] = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

START_LITERALS = Literal[
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
]

END_LITERALS = Literal[
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
    "23:59",
]


class ScheduleCog(WithBotMixin, commands.Cog, name=COG_NAME):
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
        """
        Returns the schedule for a day.
        """
        weekday_as_int = WEEKDAY_AS_INT_MAP.get(weekday, 0)
        go_weekday_as_int = time_utils.weekday_from_python_to_go(weekday_as_int)
        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                session_times: List[Tuple[time, time]] = []
                for resp in stub.GetDaySchedule(
                    ScheduleRequest(weekday=go_weekday_as_int)
                ):
                    resp: ScheduleMessage
                    session_times.append(
                        (
                            time.fromisoformat(resp.start_time),
                            time.fromisoformat(resp.end_time),
                        )
                    )
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        session_times = sorted(session_times, key=lambda x: x[0])

        embed = embeds.day_schedule(weekday, session_times)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def add_schedule_to_day(
        self,
        ctx: "Context",
        weekday: Literal[
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ],
        start_time: START_LITERALS,
        end_time: END_LITERALS,
    ):
        """
        Add a session to a day. Time must be in the format "HH:MM"
        """
        weekday_as_int = WEEKDAY_AS_INT_MAP.get(weekday, 0)

        go_weekday_as_int = time_utils.weekday_from_python_to_go(weekday_as_int)

        start_time = start_time.strip()
        end_time = end_time.strip()

        try:
            start_time_time = time.fromisoformat(start_time)
        except ValueError:
            await ctx.send(
                f"Invalid start time: {start_time}. Try the following format: '16:30'"
            )
            return

        try:
            end_time_time = time.fromisoformat(end_time)
        except ValueError:
            await ctx.send(
                f"Invalid end time: {end_time}. Try the following format: '16:30'"
            )
            return

        if end_time_time < start_time_time:
            await ctx.send(
                f"Invalid selection: End time '{end_time}' cannot be before start time '{start_time}'"
            )
            return

        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                stub.SetDaySchedule(
                    ScheduleMessage(
                        weekday=go_weekday_as_int,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        embed = embeds.day_schedule(weekday, [(start_time_time, end_time_time)])
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def add_schedule_to_day_fine(
        self,
        ctx: "Context",
        weekday: Literal[
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ],
        start_time: str,
        end_time: str,
    ):
        """
        Add a session to a day. Time must be in the format "HH:MM"
        """
        weekday_as_int = WEEKDAY_AS_INT_MAP.get(weekday, 0)

        go_weekday_as_int = time_utils.weekday_from_python_to_go(weekday_as_int)

        start_time = start_time.strip()
        end_time = end_time.strip()

        try:
            start_time_time = time.fromisoformat(start_time)
        except ValueError:
            await ctx.send(
                f"Invalid start time: {start_time}. Try the following format: '16:30'"
            )
            return

        try:
            end_time_time = time.fromisoformat(end_time)
        except ValueError:
            await ctx.send(
                f"Invalid end time: {end_time}. Try the following format: '16:30'"
            )
            return

        if end_time_time < start_time_time:
            await ctx.send(
                f"Invalid selection: End time '{end_time}' cannot be before start time '{start_time}'"
            )
            return

        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                stub.SetDaySchedule(
                    ScheduleMessage(
                        weekday=go_weekday_as_int,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        embed = embeds.day_schedule(weekday, [(start_time_time, end_time_time)])
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def clear_schedule_on_day(
        self,
        ctx: "Context",
        weekday: Literal[
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ],
    ):
        """
        Remove the schedule for a given day.
        """
        weekday_as_int = WEEKDAY_AS_INT_MAP.get(weekday, 0)
        go_weekday_as_int = time_utils.weekday_from_python_to_go(weekday_as_int)

        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = disco_pb2_grpc.DiscoStub(channel)
                stub.ClearDaySchedule(ScheduleRequest(weekday=go_weekday_as_int))
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        await ctx.send(f"Cleared schedule for {weekday}")
