import json

import requests
import disnake
from bs4 import BeautifulSoup
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands as cmd

class GitHub(cmd.Cog, name="github"):
    def __init__(self, bot):
        self.bot = bot

    @cmd.slash_command(
        name="github",
        aliases=['gh'],
        description="Get information about the Github repository.",
        options=[
            Option(
                name="owner",
                description="Repository owner.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="name",
                description="Repository name.",
                type=OptionType.string,
                required=True
            )
        ]
    )
    async def github(self, interaction: ApplicationCommandInteraction, owner: str, name: str) -> None:
        req = requests.get(f'https://api.github.com/repos/{owner}/{name}')
        apijson = json.loads(req.text)
        await interaction.response.defer(with_message=True)
        if req.status_code == 200:
            em = disnake.Embed()
            em.set_author(name=apijson['owner']['login'], icon_url=apijson['owner']['avatar_url'],
                          url=apijson['owner']['html_url'])
            em.set_thumbnail(url=apijson['owner']['avatar_url'])
            em.add_field(name="Repository:", value=f"[{apijson['name']}]({apijson['html_url']})", inline=True)
            em.add_field(name="Language:", value=apijson['language'], inline=True)

            try:
                license_url = f"[{apijson['license']['spdx_id']}]({json.loads(requests.get(apijson['license']['url']).text)['html_url']})"
            except:
                license_url = "None"
            em.add_field(name="License:", value=license_url, inline=True)
            if apijson['stargazers_count'] != 0:
                em.add_field(name="Star:", value=apijson['stargazers_count'], inline=True)
            if apijson['forks_count'] != 0:
                em.add_field(name="Fork:", value=apijson['forks_count'], inline=True)
            if apijson['open_issues'] != 0:
                em.add_field(name="Issues:", value=apijson['open_issues'], inline=True)
            em.add_field(name="Description:", value=apijson['description'], inline=False)

            for meta in BeautifulSoup(requests.get(apijson['html_url']).text, features="html.parser").find_all('meta'):
                try:
                    if meta.attrs['property'] == "og:image":
                        em.set_image(url=meta.attrs['content'])
                        break
                except:
                    pass

            await interaction.send(embed=em)
        elif req.status_code == 404:
            await interaction.send(embed=disnake.Embed(
                title="Repository not found!",
                description=f"Unable to find **{owner}/{name}**",
                color=0xE02B2B
            ))
        elif req.status_code == 503:
            await interaction.send(embed=disnake.Embed(
                title="GithubAPI down :(",
                description=f"Try later",
                color=0xE02B2B
            ))
        else:
            await interaction.send(embed=disnake.Embed(
                title="Unknown error",
                color=0xE02B2B
            ))


def setup(bot):
    bot.add_cog(GitHub(bot))