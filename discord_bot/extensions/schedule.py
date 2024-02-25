import calendar
from datetime import time
from typing import TYPE_CHECKING, List, Literal, Tuple

import grpc
from discord import Colour, Embed
from discord.ext import commands
from generated import val_go_pb2_grpc
from generated.empty_pb2 import Empty
from generated.val_go_pb2 import ScheduleMessage, ScheduleRequest, Session
from settings import SETTINGS
from utils import embeds, time_utils

from discord_bot.extensions.cog_utils import WithBotMixin

if TYPE_CHECKING:
    from discord.ext.commands import Context

import logging

log = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    await bot.remove_cog(ScheduleCog.__name__)
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


class ScheduleCog(WithBotMixin, commands.Cog):
    async def cog_load(self):
        log.info(f"Initialised {self.__cog_name__}")

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
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                session_times: List[Tuple[time, time]] = []
                resp: ScheduleMessage = stub.GetDaySchedule(
                    ScheduleRequest(weekday=go_weekday_as_int)
                )
                session_times = [
                    (
                        time.fromisoformat(session.start_time),
                        time.fromisoformat(session.end_time),
                    )
                    for session in resp.sessions
                ]
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        session_times = sorted(session_times, key=lambda x: x[0])

        embed = embeds.day_schedule(weekday, session_times)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def get_week_schedule(self, ctx: "Context"):
        """
        Get the week's schedule
        """

        days: dict[int, list[tuple[time, time]]] = {}

        try:
            with grpc.insecure_channel(
                f"localhost:{SETTINGS.python_to_go_port}"
            ) as channel:
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                for day_schedule in stub.GetWeekSchedule(Empty()):
                    day_schedule: ScheduleMessage
                    weekday = time_utils.weekday_from_go_to_python(day_schedule.weekday)
                    days[weekday] = [
                        (
                            time.fromisoformat(session.start_time),
                            time.fromisoformat(session.end_time),
                        )
                        for session in day_schedule.sessions
                    ]
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return
        embed = Embed(
            colour=Colour.blue(),
            title="📅 Week schedule",
        )
        for weekday_as_int, sessions in days.items():
            as_weekday = calendar.day_name[weekday_as_int]
            weekday_sessions = [
                f'# {i+1}: From `{session[0].strftime('%H:%M')}` until `{session[1].strftime('%H:%M')}`'
                for i, session in enumerate(sessions)
            ]
            embed.add_field(
                name=as_weekday, value="\n".join(weekday_sessions), inline=False
            )
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
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                stub.SetDaySchedule(
                    ScheduleRequest(
                        weekday=go_weekday_as_int,
                        session=Session(start_time=start_time, end_time=end_time),
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
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                stub.SetDaySchedule(
                    ScheduleRequest(
                        weekday=go_weekday_as_int,
                        session=Session(
                            start_time=start_time,
                            end_time=end_time,
                        ),
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
                stub = val_go_pb2_grpc.ValheimGoStub(channel)
                stub.ClearDaySchedule(ScheduleRequest(weekday=go_weekday_as_int))
        except grpc.RpcError as rpc_error:
            await ctx.send(f"Failed to start server: {rpc_error}")
            return

        await ctx.send(f"Cleared schedule for {weekday}")
