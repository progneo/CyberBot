import os
from os.path import join, dirname
import time 
import json
import requests
import platform
import random

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands as cmd
from disnake.ext import tasks
from disnake.ext.commands import Bot
from disnake.ext.commands import Context
from dotenv import load_dotenv

import cyberbot
from cyberbot.exceptions import *

req = requests.get(f'https://api.github.com/repos/ProgNeo/CyberBot/tags')
response = json.loads(req.text)
"""
if req.status_code == 200:
    if response[0]['name'] == cyberbot.version():
        print("You are currently running the latest version of CyberBot!\n")
    else:
        version_listed = False
        for x in response:
            if x['name'] == cyberbot.version():
                version_listed = True
                print("You are not using our latest version! :(\n")
        if not version_listed:
            print("You are currently using an unlisted version!\n")
elif req.status_code == 404:
    # 404 Not Found
    print("Latest cyberbot.py version not found!\n")
elif req.status_code == 500:
    # 500 Internal Server Error
    print("An error occurred while fetching the latest cyberbot.py version. [500 Internal Server Error]\n")
elif req.status_code == 502:
    # 502 Bad Gateway
    print("An error occurred while fetching the latest cyberbot.py version. [502 Bad Gateway]\n")
elif req.status_code == 503:
    # 503 Service Unavailable
    print("An error occurred while fetching the latest cyberbot.py version. [503 Service Unavailable]\n")
else:
    print("An unknown error has occurred when fetching the latest cyberbot.py version\n")
    print("HTML Error Code:" + str(req.status_code))
"""

load_dotenv(join(dirname(__file__), '.env'))

if os.getenv('CONFIG_VERSION') != cyberbot.config_version():
    if os.path.isfile('.env'):
        print("Missing environment variables. Please backup and delete .env, then run CyberBot.py again.")
        quit(2)
    print("Unable to find required environment variables. Running setup.py...")
    cyberbot.setup.__init__()
    
print("Initializing bot...")

intents = disnake.Intents.default()

bot = cmd.Bot(intents=intents, help_command=None)

print(f"""
   ______      __              ____        __ 
  / ____/_  __/ /_  ___  _____/ __ )____  / /_
 / /   / / / / __ \/ _ \/ ___/ __  / __ \/ __/
/ /___/ /_/ / /_/ /  __/ /  / /_/ / /_/ / /_  
\____/\__, /_____/\___/_/  /_____/\____/\__/  
     /____/                      by ProgNeo  
-------------------
Discord.py API version: {disnake.__version__}
Python version: {platform.python_version()}
Running on: {platform.system()} {platform.release()} ({os.name})
Version: {cyberbot.version()}   
-------------------""")

@bot.event
async def on_ready():
    status_task.start()
    print(f"Connected to Discord API in {round(time.perf_counter() - discord_time_start, 2)}s")
    print("-------------------")
    for guild in bot.guilds:
        # TODO: add guilds to database
        pass


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    statuses = [f"dev"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))
    
    
def load_commands() -> None:
    for file in os.listdir(f"./cyberbot/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cyberbot.cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")
    print("-------------------")

    
@bot.event
async def on_message(message: disnake.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    print(
        f"Executed {interaction.data.name} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.author} (ID: {interaction.author.id})")


@bot.event
async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
    if isinstance(error, UserBlacklisted):
        embed = disnake.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B
        )
        print("A blacklisted user tried to execute a command.")
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, cmd.errors.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        print("A blacklisted user tried to execute a command.")
        return await interaction.send(embed=embed, ephemeral=True)
    raise error


@bot.event
async def on_command_completion(context: Context) -> None:
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")


@bot.event
async def on_command_error(context: Context, error) -> None:
    if isinstance(error, cmd.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = disnake.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, cmd.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, cmd.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error


if __name__ == "__main__":
    load_commands()
    
try:
    discord_time_start = time.perf_counter()
    bot.run(cyberbot.config.bot_token())
except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    time.sleep(5)
    exit(1)