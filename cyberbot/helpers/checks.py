import cyberbot

from typing import TypeVar, Callable
from disnake.ext import commands
from exceptions import *

T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    async def predicate(context: commands.Context) -> bool:
        if str(context.author.id) != cyberbot.config.bot_owner:
            raise UserNotOwner
        return True

    return commands.check(predicate)