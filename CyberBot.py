import os
import time 
from os.path import join, dirname
import json
import requests

import discord
from discord.ext import commands as dcmd
from dotenv import load_dotenv

import cyberbot

print(f"""
   ______      __              ____        __ 
  / ____/_  __/ /_  ___  _____/ __ )____  / /_
 / /   / / / / __ \/ _ \/ ___/ __  / __ \/ __/
/ /___/ /_/ / /_/ /  __/ /  / /_/ / /_/ / /_  
\____/\__, /_____/\___/_/  /_____/\____/\__/  
     /____/                      by ProgNeo  
     
     
     
Version: {cyberbot.version()}        
""")

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

intents = discord.Intents.default()
intents.members = True
intents.typing = False
bot = dcmd.Bot(intents=intents, command_prefix=cyberbot.config.bot_prefix(), help_command=None)

@bot.event
async def on_ready():
    print(f"Connected to Discord API in {round(time.perf_counter() - discord_time_start, 2)}s")
    time_start = time.perf_counter()
    # TODO: load cogs
    cyberbot.events.__init__(bot)
    for guild in bot.guilds:
        # TODO: add guilds to database
        pass
    print(f"Registered commands and events in {round(time.perf_counter() - time_start, 2)}s")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(cyberbot.config.bot_status()))  # Update Bot status


try:
    discord_time_start = time.perf_counter()
    bot.run(cyberbot.config.bot_token())
except Exception as e:
    print(f"[/!\\] Error: Failed to connect to DiscordAPI. Please check your bot token!\n{e}")
    time.sleep(5)
    exit(1)