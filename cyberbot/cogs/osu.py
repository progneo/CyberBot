import json
import disnake

import requests
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands as cmd

import cyberbot
from cyberbot.helpers.messages import error_message


class OsuPlayer:
    def __init__(self, player) -> None:
        self.id = player["user_id"]
        self.username = player["username"]
        self.join_date = (player["join_date"].split(" "))[0]
        self.c300 = player["count300"]
        self.c100 = player["count100"]
        self.c50 = player["count50"]
        self.playcount = player["playcount"]
        self.ranked = player["ranked_score"]
        self.total = player["total_score"]
        self.pp = player["pp_rank"]
        self.level = player["level"]
        self.pp_raw = player["pp_raw"]
        self.accuracy = player["accuracy"]
        self.count_ss = player["count_rank_ss"]
        self.count_s = player["count_rank_s"]
        self.count_a = player["count_rank_a"]
        self.country = player["country"]
        self.pp_country_rank = player["pp_country_rank"]

    def get_embed_info(self, author) -> disnake.Embed:
        em = disnake.Embed(color=0xff00ff)
        em.set_author(name=f"{self.country.upper()} | {self.username}", url=f"https://osu.ppy.sh/u/{self.username}")
        em.add_field(name='Performance', value=self.pp_raw + 'pp')
        em.add_field(name='Accuracy', value="{0:.2f}%".format(float(self.accuracy)))
        lvl = int(float(self.level))
        percent = int((float(self.level) - lvl) * 100)
        em.add_field(name='Level', value=f"{lvl} ({percent}%)")
        em.add_field(name='Rank', value=self.pp)
        em.add_field(name='Country Rank', value=self.pp_country_rank)
        em.add_field(name='Playcount', value=self.playcount)
        return em


class Osu(cmd.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cmd.slash_command(
        name="osu",
        description="Get information about an osu! player. (it looks terrible now)", 
        options=[
            Option(
                name="name",
                description="Username of osu! player.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="mode",
                description="Game mode (std: 0, taiko: 1, ctb: 2, mania: 3).",
                type=OptionType.integer,
                required=False,
                min_value=0,
                max_value=3
            ),
        ],
    )
    async def osu(self, interaction: ApplicationCommandInteraction, name: str, mode: int = 0) -> None:
        r = requests.get(f'https://osu.ppy.sh/api/get_user?k={cyberbot.config.osu_api_key()}&u={name}&m={mode}')
        if r.status_code != 200:
            print('Osu API Debug: ' + str(r.status_code) + ' | ' + r.text)
            if r.status_code == 401:
                embed=error_message(description="Invalid osu!api key. Please contact your server owner.")
                await interaction.send(embed=embed, ephemeral=True)
            else:
                embed = error_message(description=f"Failed to fetch osu!api data. ({str(r.status_code)})")
                await interaction.send(embed=embed, ephemeral=True)
            return

        user = json.loads(r.text)
        if len(user) < 1:
            embed = error_message(description=f"osu! player **{name}** not found.")
            
            await interaction.send(embed=embed)
            return
        
        embed = OsuPlayer(user[0]).get_embed_info(interaction.author)
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))