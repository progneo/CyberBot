import aiohttp
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands as cmd

import cyberbot
from cyberbot.helpers.messages import default_message

class Fun(cmd.Cog, name="Fun"):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @cmd.slash_command(
        name="wink",
        description="Wink."
    )
    async def wink(self, interaction: ApplicationCommandInteraction) -> None:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/animu/wink') as r:
                res = await r.json()
                imgUrl = res['link']
        embed = default_message().set_image(url=imgUrl)
        await interaction.send(embed=embed)
        
    @cmd.slash_command(
        name="pat",
        description="Pet someone.",
        options=[
            Option(
                name="user",
                description="The user you want to pet.",
                type=OptionType.user,
                required=True
            )
        ]
    )
    async def pat(self, interaction: ApplicationCommandInteraction, user: disnake.User) -> None:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/animu/pat') as r:
                res = await r.json()
                imgUrl = res['link']        
        embed = default_message(
            title=f'{interaction.author.name} stroked {user.name}'
        ).set_image(url=imgUrl)
        await interaction.send(embed=embed)
        
    @cmd.slash_command(
        name="hug",
        description="Hug someone.",
        options=[
            Option(
                name="user",
                description="The user you want to hug.",
                type=OptionType.user,
                required=True
            )
        ]
    )
    async def hug(self, interaction: ApplicationCommandInteraction, user: disnake.User) -> None:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/animu/hug') as r:
                res = await r.json()
                imgUrl = res['link']        
        embed = default_message(
            title=f'{interaction.author.name} hugged {user.name}',
        ).set_image(url=imgUrl)
        await interaction.send(embed=embed)
    
    @cmd.slash_command(
        name="avatar",
        description="Show the user's avatar.",
        options=[
            Option(
                name="user",
                description="The user whose avatar you want to see.",
                type=OptionType.user,
                required=False
            )
        ]
    )
    async def avatar(self, interaction: ApplicationCommandInteraction, user: disnake.User = None) -> None:
        if user is None:
            user = interaction.author
        embed = default_message(
            title=f"{user.display_name}'s avatar.", 
            color=user.accent_color
        ).set_image(url=user.avatar)
        await interaction.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Fun(bot))