import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands as cmd

from cyberbot.helpers.messages import default_message, error_message


class Moderation(cmd.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @cmd.slash_command(
        name="purge",
        description="Delete a number of messages.",
        options=[
            Option(
                name="amount",
                description="The amount of messages you want to delete. (Must be between 1 and 100.)",
                type=OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ],
    )
    @cmd.has_guild_permissions(manage_messages=True)
    async def purge(self, interaction: ApplicationCommandInteraction, amount: int) -> None:
        purged_messages = await interaction.channel.purge(limit=amount)
        embed = default_message(
            title="Chat Cleared!",
            description=f"**{interaction.author}** cleared **{len(purged_messages)}** messages!",
        )
        await interaction.send(embed=embed, ephemeral=True)
        
    @cmd.slash_command(
        name="kick",
        description="Kick a user out of server.",
        options=[
            Option(
                name="user",
                description="The user you want to kick.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you kicked the user.",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @cmd.has_permissions(kick_members=True)
    async def kick(self, interaction: ApplicationCommandInteraction, 
                   user: disnake.User,
                   reason: str = "Not specified") -> None:
        member = await interaction.guild.get_or_fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = error_message(
                description="User has Admin permissions."
            )
            await interaction.send(embed=embed)
        else:
            try:
                embed = default_message(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{interaction.author}**!"
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{interaction.author}**!\nReason: {reason}"
                    )
                except disnake.Forbidden:
                    pass
                await member.kick(reason=reason)
            except:
                embed = error_message(
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                )
                await interaction.send(embed=embed, ephemeral=True)
            
    @cmd.slash_command(
        name="nick",
        description="Change the nickname of a user on a server.",
        options=[
            Option(
                name="user",
                description="The user you want to change the nickname.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="nickname",
                description="The new nickname of the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @cmd.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: ApplicationCommandInteraction, user: disnake.User, nickname: str = None) -> None:
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = default_message(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
            )
            await interaction.send(embed=embed)
        except:
            embed = error_message(
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname."
            )
            await interaction.send(embed=embed, ephemeral=True)
            
    @cmd.slash_command(
        name="ban",
        description="Bans a user from the server.",
        options=[
            Option(
                name="user",
                description="The user you want to ban.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you banned the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @cmd.has_permissions(ban_members=True)
    async def ban(self, interaction: ApplicationCommandInteraction, user: disnake.User, reason: str = "Not specified") -> None:
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = error_message(
                    description="User has Admin permissions."
                )
                await interaction.send(embed=embed)
            else:
                embed = default_message(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{interaction.author}**!"
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(f"You were banned in guild **{interaction.guild.name}** by **{interaction.author}**!\nReason: {reason}")
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = error_message(
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban."
            )
            await interaction.send(embed=embed, ephemeral=True)
       
       
def setup(bot):
    bot.add_cog(Moderation(bot))