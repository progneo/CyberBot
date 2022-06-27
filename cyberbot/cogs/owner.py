import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from cyberbot.helpers import checks


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)
        await self.bot.close()

    @commands.slash_command(
        name="say",
        description="The bot will say anything you want.",
        options=[
            Option(
                name="message",
                description="The message you want me to repeat.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def say(self, interaction: ApplicationCommandInteraction, message: str) -> None:
        await interaction.send(message)

    @commands.slash_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
        options=[
            Option(
                name="message",
                description="The message you want me to repeat.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    @checks.is_owner()
    async def embed(self, interaction: ApplicationCommandInteraction, message: str) -> None:
        embed = disnake.Embed(
            description=message,
            color=0x9C84EF
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))