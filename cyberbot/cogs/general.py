import cyberbot
import disnake
import aiohttp
from disnake import ApplicationCommandInteraction
from disnake.ext import commands as cmd

from cyberbot.helpers.messages import default_message, error_message

class General(cmd.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot: disnake.Client = bot
        
    @cmd.slash_command(
        name="about",
        description="Get information about bot."
    )
    async def info(self, interaction: ApplicationCommandInteraction) -> None:
        embed = default_message(
            title=f"CyberBot {cyberbot.version()}", 
            description="Discord bot with gambling, listening to music, moderation and other interesting things."
        )
        embed.set_author(
            name=f"Developer: ProgNeo#1817",
            icon_url="https://avatars.githubusercontent.com/u/43195117?v=4"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/app-icons/612885675238359042/b1da2d7b58a2f8f8e7723a20222c8f9b.png?size=256"
        )
        embed.add_field(
            name="Bot User:", 
            value=self.bot.user
        )
        embed.add_field(
            name="Guilds:", 
            value=str(len(self.bot.guilds))
        )
        members_count = 0
        for guild in self.bot.guilds:
            members_count += guild.member_count
        embed.add_field(
            name="Members:", 
            value=str(members_count)
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
        
        embed = default_message(
            title="**Server Name:**",
            description=f"{interaction.guild}"
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
        embed = default_message(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms."
        )
        await interaction.send(embed=embed)
    
    @cmd.slash_command(
        name="invite",
        description="Get the invite link of the bot."
    )
    async def invite(self, interaction: ApplicationCommandInteraction) -> None:
        invite = default_message(
            title="Invite link",
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?client_id=612885675238359042&permissions=8&scope=bot)",
            color=0xD75BF4
        )
        try:
            await interaction.author.send(embed=invite)
            embed = default_message(
                title="Success",
                description=f"Check your private messages",
            )
            await interaction.send(embed=embed, ephemeral=True)
            
        except disnake.Forbidden:
            await interaction.send(embed=invite, ephemeral=True)
            
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
                    embed = default_message(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:"
                    )
                else:
                    embed = error_message(
                        description="There is something wrong with the API, please try again later",
                    )
                await interaction.send(embed=embed, ephemeral=True)
                
                
def setup(bot):
    bot.add_cog(General(bot))