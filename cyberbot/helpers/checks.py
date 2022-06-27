import cyberbot

from typing import TypeVar, Callable
from disnake.ext import commands

from cyberbot.exceptions import *

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    async def predicate(context: commands.Context) -> bool:
        if context.author.id != cyberbot.config.bot_owner():
            raise UserNotOwner
        return True

    return commands.check(predicate)

def is_nswf() -> Callable[[T], T]:
    async def predicate(context: commands. Context) -> bool:
        if not context.channel.nsfw:
            raise ChannelNotNsfw
        return True
    
    return commands.check(predicate)