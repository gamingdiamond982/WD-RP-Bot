from typing import Coroutine
import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot
from accounting import Server
from datetime import datetime
import time
import logging
import argparse
from economy import shop

_commands = []  # an array of command callables
_events = []
_server = None
_bot = None
logger = logging.getLogger(__name__)


def get_bot() -> Bot:
    return _bot


def get_server() -> Server:
    return _server


def register_commands(bot: commands.Bot, s: Server):
    global _server
    global _bot
    _bot = bot
    _server = s
    for i in _commands:
        bot.add_command(i)

    for i in _events:
        bot.event(i)


def _add_event(event: Coroutine):
    _events.append(event)


def _add_command(cmd: Coroutine):
    _commands.append(cmd)


@commands.command(name="balance")
async def _balance(ctx: Context, *args, **kwargs):
    raise NotImplementedError()


_add_command(_balance)


@commands.command(name="ping")
async def _ping(ctx: Context, *args, **kwargs):
    await ctx.reply(
        f'Pong! - took me {round((time.time() - datetime.timestamp(ctx.message.created_at)) * 1000, 2)}ms to send a response')


_add_command(_ping)


@commands.command(name="shop")
async def _shop(ctx: Context, *args, **kwargs):
    await shop.shop(ctx, get_server())


_add_command(_shop)


async def on_reaction_add(reaction, user):
    await shop.buy(reaction, user, get_server(), get_bot())


_add_event(on_reaction_add)
