import time

import cyberbot


def __init__():
    print("NOTE: You can change the settings later in .env")

    # Declare default configuration
    input_db_host = "127.0.0.1"
    input_db_database = "cyberbot"
    input_db_user = "root"
    input_db_password = ""

    input_bot_token = input("Discord bot token: ")
    input_bot_prefix = input("Command Prefix: ")
    input_bot_status = input("Bot status: (Playing xxx) ")
    input_db_host = input("Database Host: ")
    input_db_database = input("Database name: ")
    input_db_user = input("Database User: ")
    input_db_password = input("Database Password: ")
    input_lavalink_host = input("Lavalink Host: ")
    input_lavalink_port = input("Lavalink Port: ")
    input_lavalink_password = input("Lavalink Password: ")

    try:
        config = f"""CONFIG_VERSION=0.1
BOT_TOKEN={input_bot_token}
BOT_PREFIX={input_bot_prefix}
BOT_STATUS={input_bot_status}
DB_HOST={input_db_host}
DB_DATABASE={input_db_database}
DB_USER={input_db_user}
DB_PASSWORD={input_db_password}
LAVALINK_HOST={input_lavalink_host}
LAVALINK_PORT={input_lavalink_port}
LAVALINK_PASSWORD={input_lavalink_password}
"""
        open('./.env', 'w').write(config)
        print("\n[*] Successfully created .env file!")
        print("CyberBot.py setup complete! Starting bot in 5 seconds...")
        time.sleep(5)
        print('\n' * 100)
    except Exception as e:
        print("\n[!] An error occurred when creating config file.\n" + str(e))
        quit()