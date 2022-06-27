import json
import cyberbot
import disnake
from profanity_check import predict_prob
from disnake.ext import commands as cmd


class Events(cmd.Cog, name="Events"):
    def __init__(self, bot):
        self.bot = bot

    @self.bot.event
    async def on_member_join(self, member):
        # TODO: something idk
        pass


def leave(bot):
    @bot.event
    async def on_member_remove(member):
        # TODO: something idk
        pass


def on_guild_join(bot):
    @bot.event
    async def on_guild_join(ctx):
        # TODO: something idk
        pass


def message_send(bot):
    @bot.event
    async def on_message(message):
        # TODO: add exp
        pass
        await bot.process_commands(message)

    @bot.event
    async def on_message(message):
        punctuations = '!()-[]{};:\'"\\,<>./?@#$%^&*_~'
        # remove punctuation from the string
        msg = ""
        for char in message.content.lower():
            if char not in punctuations:
                msg = msg + char

        # profanity check
        prob = predict_prob([msg])
        if prob >= 0.8:
            em = disnake.Embed(title=f"AI Analysis Results", color=0xC54B4F)
            em.add_field(name='PROFANITY DETECTED! ', value=str(prob[0]))
            await message.channel.send(embed=em)

        await bot.process_commands(message)


def message_edit(bot):
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


def message_delete(bot):
    @bot.event
    async def on_message_delete(ctx):
        # TODO: log it
        pass


def on_command_error(bot):
    @bot.event
    async def on_command_error(ctx, e):
        # TODO: log it
        pass