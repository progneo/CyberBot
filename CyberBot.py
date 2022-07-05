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
from cyberbot.helpers.messages import error_message
from cyberbot.managers.database import Database

req = requests.get(f'https://api.github.com/repos/ProgNeo/CyberBot/tags')
response = json.loads(req.text)

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
Disnake.py API version: {disnake.__version__}
Python version: {platform.python_version()}
Running on: {platform.system()} {platform.release()} ({os.name})
Version: {cyberbot.version()}   
-------------------""")

@bot.event
async def on_ready():
    print(f"Connected to Discord API in {round(time.perf_counter() - discord_time_start, 2)}s")
    status_task.start()
    
    database = connect_database()
    load_commands(database)
    
    for guild in bot.guilds:
        # TODO: add guilds to database
        pass


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    statuses = [f"dev"]
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))
    
    
def load_commands(database: Database) -> None:
    cyberbot.events.__init__(bot, database)
    cyberbot.cogs.anime.setup(bot)
    cyberbot.cogs.fun.setup(bot)
    cyberbot.cogs.general.setup(bot)
    cyberbot.cogs.github.setup(bot)
    cyberbot.cogs.moderation.setup(bot)
    cyberbot.cogs.osu.setup(bot)
    cyberbot.cogs.owner.setup(bot)
    
    
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
        embed = error_message(description="You are blacklisted from using the bot.")
        print("A blacklisted user tried to execute a command.")
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, cmd.errors.MissingPermissions):
        embed = error_message(description=f"You are missing the permission {error.missing_permissions} to execute this command!")
        print("A blacklisted user tried to execute a command.")
        return await interaction.send(embed=embed, ephemeral=True)
    raise error


def connect_database() -> Database:
    time_start = time.perf_counter()
    database = Database()
    database.create_tables()
    print(f"Connected to database ({cyberbot.config.db_host()}) in {round(time.perf_counter() - time_start, 2)}s")
    print("-------------------")
    return database
  
    
try:
    discord_time_start = time.perf_counter()
    bot.run(cyberbot.config.bot_token())
except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    time.sleep(5)
    exit(1)