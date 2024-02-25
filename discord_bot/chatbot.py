import asyncio
import logging

import discord
import grpc
from discord.ext import commands
from discoserver import ValheimPyServer
from generated import val_py_pb2_grpc
from settings import SETTINGS

log = logging.getLogger(__name__)

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

chat_bot = commands.Bot(command_prefix="$", intents=intents)

extensions = ["lifecycle", "players", "channel", "schedule", "helpers"]


@chat_bot.event
async def on_ready():
    log.info("Logged in")
    for ext in extensions:
        await chat_bot.load_extension(f"extensions.{ext}")


async def serve_grpc():
    server = grpc.aio.server()
    val_py_pb2_grpc.add_ValheimPyServicer_to_server(ValheimPyServer(chat_bot), server)
    server.add_insecure_port(f"localhost:{SETTINGS.go_to_python_port}")
    await server.start()
    await server.wait_for_termination()


async def startup():
    discord.utils.setup_logging()
    async with asyncio.TaskGroup() as tg:
        chatbot_task = tg.create_task(chat_bot.start(token=SETTINGS.bot_token))
        grpc_task = tg.create_task(serve_grpc())
    try:
        await asyncio.gather(chatbot_task, grpc_task)
    except asyncio.CancelledError:
        # Task was cancelled
        pass
    except Exception as e:
        log.info(f"Got exception: {e}")
        pass
    finally:
        log.info("Finishing task group")


if __name__ == "__main__":
    asyncio.run(startup())
