import io
import json
import random 
from optparse import Option

import aiohttp
import disnake
import requests
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands as cmd

import cyberbot


class Anime(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot

    def neko_api(self, interaction: ApplicationCommandInteraction, x):
        try:
            req = requests.get(f'https://nekos.life/api/v2/img/{x}')
            if req.status_code != 200:
                print("Could not get a neko")
            apijson = json.loads(req.text)
            url = apijson["url"]
            em = disnake.Embed(
                color=0x9C84EF,
            )
            em.set_image(url=url)
            return em
        except:
            return disnake.Embed(
                title="Error!",
                description=f"Can't obtain image ({req.status_code})",
                color=0xE02B2B
            )

    @cmd.slash_command(
        name="anime",
        description="The bot will send a random anime picture/gif.",
        options=[
            Option(
                name="type",
                description="Type of picture.",
                type=OptionType.string,
                required=False
            )
        ]
    )
    async def anime(self, interaction: ApplicationCommandInteraction, type: str = None) -> None:
        api_types = [
            'smug', 'gasm', '8ball', 'cuddle', 'avatar', 'slap', 
            'pat', 'gecg', 'feed', 'fox_girl', 'lizard', 'neko', 'hug', 
            'kiss', 'wallpaper', 'tickle', 'spank', 'waifu', 'lewd'
        ]
        if (type == None):
            type = random.choice(api_types)
        if (type in api_types):
            await interaction.send(embed=self.neko_api(interaction, type))
        else:
            await interaction.send(
                embed=disnake.Embed(
                    title="Invalid argument!",
                    description=f"Valid argument(s): ``{api_types}``",
                    color=0xE02B2B
                ),
                ephemeral=True
            )
                

def setup(bot):
    bot.add_cog(Anime(bot))