from typing import Coroutine
import cyberbot
import asyncpg
import asyncio

async def __init__():
    try:
        credentials = {
            "user": cyberbot.config.db_user, 
            "password": cyberbot.config.db_password, 
            "database": cyberbot.config.db_database, 
            "host": cyberbot.config.db_host
        }
        db = await asyncpg.create_pool(**credentials)
        return (db)
    except Exception as error:
        print("\nUnable to connect to database. Please check your credentials!\n" + str(error) + "\n")
        quit()