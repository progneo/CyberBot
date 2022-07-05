import disnake
from disnake.ext import commands as cmd

from cyberbot.managers.database import Database

def __init__(bot: disnake.Client, database: Database):
    join(bot, database)
    leave(bot, database)
    on_guild_join(bot, database)
    message_send(bot, database)
    message_edit(bot, database)
    message_delete(bot, database)


def join(bot: disnake.Client, database: Database):
    @bot.event
    async def on_member_join(self, member):
        # TODO: something idk
        pass


def leave(bot: disnake.Client, database: Database):
    @bot.event
    async def on_member_remove(member):
        # TODO: something idk
        pass


def on_guild_join(bot: disnake.Client, database: Database):
    @bot.event
    async def on_guild_join(ctx):
        # TODO: something idk
        pass


def message_send(bot: disnake.Client, database: Database):
    @bot.event
    async def on_message(message):
        # TODO: add exp
        pass
        await bot.process_commands(message)


def message_edit(bot: disnake.Client, database: Database):
    @bot.event
    async def on_raw_message_edit(ctx):
        # TODO: something idk
        pass


def message_delete(bot: disnake.Client, database: Database):
    @bot.event
    async def on_message_delete(ctx):
        # TODO: log it
        pass


def on_command_error(bot: disnake.Client, database: Database):
    @bot.event
    async def on_command_error(ctx, e):
        # TODO: log it
        pass