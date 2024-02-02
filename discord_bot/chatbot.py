import asyncio
import discord
import grpc
from discord.ext import commands
from discoserver import DiscoServer
from generated import disco_pb2_grpc
from settings import SETTINGS

import logging

log = logging.getLogger(__name__)


intents = discord.Intents.default()

intents.message_content = True
intents.members = True

chat_bot = commands.Bot(command_prefix="$", intents=intents)


queue = asyncio.Queue()


@chat_bot.event
async def on_ready():
    log.info("Logged in")
    await setup_bot(chat_bot)


async def setup_bot(x: commands.Bot):
    await x.load_extension("extensions.reloader")
    await x.load_extension("extensions.sync")
    await x.load_extension("extensions.lifecycle")
    await x.load_extension("extensions.registrar")
    await x.load_extension("extensions.channel")
    await x.load_extension("extensions.schedule")


async def serve_grpc():
    server = grpc.aio.server()
    disco_pb2_grpc.add_DiscoServicer_to_server(DiscoServer(chat_bot), server)
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


