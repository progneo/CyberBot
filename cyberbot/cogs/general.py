import cyberbot
import disnake
import aiohttp
from disnake import ApplicationCommandInteraction
from disnake.ext import commands as cmd

import cyberbot

class General(cmd.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
        
    @cmd.slash_command(
        name="about",
        description="Get information about bot."
    )
    async def info(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            title="Developer: @ProgNeo", 
            description="Discord Bot",
            color=0x9C84EF
        )
        embed.set_author(
            name=f"CyberBot {cyberbot.version()}",
            icon_url="https://cdn.discordapp.com/avatars/612885675238359042/ec6ab32d43d62b0a03bb6b3dabdb0b1f.png?size=256"
        )
        embed.set_thumbnail(
            url="https://avatars.githubusercontent.com/u/43195117?v=4"
        )
        embed.add_field(
            name="Bot User:", 
            value=self.bot.user
        )
        embed.add_field(
            name="Guilds:", 
            value=str(len(self.bot.guilds))
        )
        embed.add_field(
            name="Members:", 
            value=str(len(set(self.bot.get_all_members())))
        )
        embed.add_field(
            name="O.S.:", 
            value=str(cyberbot.getPlatform())
        )
        embed.add_field(
            name="Github Repo:", 
            value="[CyberBot](https://github.com/ProgNeo/CyberBot)"
        )
        embed.add_field(
            name="Bug Report:", 
            value="[Issues](https://github.com/ProgNeo/CyberBot/issues)")
        embed.add_field(
            name="Links",
            value="[Support Discord](https://discord.gg/TpezxsmpkY) | [Add bot to server]("
                    "https://discordapp.com/oauth2/authorize?client_id=612885675238359042&permissions=8&scope=bot)",
            inline=False
        )
        embed.set_footer(
            text=f"{cyberbot.copyright()} | Code licensed under the MIT License"
        )
        await interaction.send(embed=embed)
        
    @cmd.slash_command(
        name="severinfo",
        description="Get information about server.",
        alias="server"
    )
    async def serverinfo(self, interaction: ApplicationCommandInteraction) -> None:
        roles = [role.name for role in interaction.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f"[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        
        embed = disnake.Embed(
            title="**Server Name:**",
            description=f"{interaction.guild}",
            color=0x9C84EF
        )
        embed.set_thumbnail(
            url=interaction.guild.icon.url
        )
        embed.add_field(
            name="Server ID",
            value=interaction.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=interaction.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(interaction.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(interaction.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {interaction.guild.created_at}"
        )
        await interaction.send(embed=embed)
         
    @cmd.slash_command(
        name="ping",
        description="Check bot latency."
    )
    async def ping(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)
    
    @cmd.slash_command(
        name="invite",
        description="Get the invite link of the bot."
    )
    async def invite(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?client_id=612885675238359042&permissions=8&scope=bot",
            color=0xD75BF4
        )
        try:
            await interaction.author.send(embed=embed)
            await interaction.send("I sent you a private message!")
        except disnake.Forbidden:
            await interaction.send(embed=embed)
            
    @cmd.slash_command(
        name="bitcoin",
        description="Get the price of bitcoin."
    )
    async def bitcoin(self, interaction: ApplicationCommandInteraction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")
                    embed = disnake.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0x9C84EF
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                await interaction.send(embed=embed)
                
                
def setup(bot):
    bot.add_cog(General(bot))