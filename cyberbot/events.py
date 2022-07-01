import json
import cyberbot
import disnake
from disnake.ext import commands as cmd


def join(bot: disnake.Client):
    @bot.event
    async def on_member_join(self, member):
        # TODO: something idk
        pass


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
    async def on_message(message):
        # TODO: add exp
        pass
        await bot.process_commands(message)


def message_edit(bot: disnake.Client):
    @bot.event
    async def on_raw_message_edit(ctx):
        guild_id = json.loads(json.dumps(ctx.data))['guild_id']
        channel_id = json.loads(json.dumps(ctx.data))['channel_id']
        message_id = json.loads(json.dumps(ctx.data))['id']
        try:
            author_id = json.loads(json.dumps(json.loads(json.dumps(ctx.data))['author']))['id']
            content = json.loads(json.dumps(ctx.data))['content']
            # TODO: log it
            pass
        except:
            content = str(json.loads(json.dumps(ctx.data))['embeds'])


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