import random 
import disnake
from disnake.ext import commands as cmd

import cyberbot
from cyberbot import default_message

def __init__(bot: disnake.Client):
    join(bot)
    leave(bot)
    on_guild_join(bot)
    message_send(bot)
    message_edit(bot)
    message_delete(bot)


def join(bot: disnake.Client):
    @bot.event
    async def on_member_join(member: disnake.Member):
        channel_id = cyberbot.database.get_greetings_channel(member.guild)
        if channel_id != 0:
            channel: disnake.TextChannel = bot.get_channel(channel_id)
            channel.send(embed=default_message("New member!", f"Welcome, {member.mention}!").set_thumbnail(member.avatar))
            cyberbot.add_user(member)


def leave(bot: disnake.Client):
    @bot.event
    async def on_member_remove(member):
        # TODO: something idk
        pass


def on_guild_join(bot: disnake.Client):
    @bot.event
    async def on_guild_join(ctx):
        # TODO: something idk
        pass


def message_send(bot: disnake.Client):
    @bot.event
    async def on_message(message: disnake.Message):
        cyberbot.database.change_xp(message.author, random.randrange(1, 5))


def message_edit(bot: disnake.Client):
    @bot.event
    async def on_raw_message_edit(ctx):
        # TODO: something idk
        pass


def message_delete(bot: disnake.Client):
    @bot.event
    async def on_message_delete(ctx):
        # TODO: log it
        pass


def on_command_error(bot: disnake.Client):
    @bot.event
    async def on_command_error(ctx, e):
        # TODO: log it
        pass