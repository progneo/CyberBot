import time

import cyberbot


def __init__():
    print("NOTE: You can change the settings later in .env")

    bot_token = input("Discord bot token: ")
    db_host = input("Database Host: ")
    db_database = input("Database name: ")
    db_user = input("Database User: ")
    db_password = input("Database Password: ")
    lavalink_host = input("Lavalink Host: ")
    lavalink_port = input("Lavalink Port: ")
    lavalink_password = input("Lavalink Password: ")
    osu_api_key = input("osu! api key: ")

    try:
        config = f"""CONFIG_VERSION=0.1
BOT_TOKEN={bot_token}
DB_HOST={db_host}
DB_DATABASE={db_database}
DB_USER={db_user}
DB_PASSWORD={db_password}
LAVALINK_HOST={lavalink_host}
LAVALINK_PORT={lavalink_port}
LAVALINK_PASSWORD={lavalink_password}
OSU_API_KEY={osu_api_key}
"""
        open('./.env', 'w').write(config)
        print("\n[*] Successfully created .env file!")
        print("CyberBot.py setup complete! Starting bot in 5 seconds...")
        time.sleep(5)
        print('\n' * 100)
    except Exception as e:
        print("\n[!] An error occurred when creating config file.\n" + str(e))
        quit()