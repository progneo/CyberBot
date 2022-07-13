import os
import disnake
import mysql.connector
from contextlib import closing


def connect():
    MYSQL_DB_DATABASE = os.environ.get('DB_DATABASE')
    MYSQL_DB_HOST = os.environ.get('DB_HOST')
    MYSQL_DB_USER = os.environ.get('DB_USER')
    MYSQL_DB_PASSWORD = os.environ.get('DB_PASSWORD')
    try:
        return mysql.connector.connect(
            db=MYSQL_DB_DATABASE,
            host=MYSQL_DB_HOST,
            user=MYSQL_DB_USER,
            password=MYSQL_DB_PASSWORD
        )
    except Exception as e:
        print("\nUnable to connect to database. Please check your credentials!\n" + str(e) + "\n")
        quit()


def create_tables() -> None:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `greetings_channel_id` BIGINT, `log_channel_id` BIGINT)')
            cursor.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `balance` BIGINT, `xp` INT, `lvl` INT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS `bot_logs` (`timestamp` TEXT, `type` TINYTEXT, `class` TINYTEXT, `message` MEDIUMTEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS `guild_logs` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS `blacklist` (`guild_id` BIGINT, `user_id` BIGINT, `reason` MEDIUMTEXT)")
            db.commit()


def get_guild(guild: disnake.Guild) -> tuple:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            return cursor.execute(f"SELECT * FROM `guilds` WHERE guild_id = {guild.id}").fetchone()


def add_guild(guild: disnake.Guild) -> None:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            cursor.execute(f"SELECT * FROM `guilds` WHERE guild_id = {guild.id}")
            if cursor.rowcount == 0:
                cursor.execute(f"INSERT INTO `guilds` (guild_id, greetings_channel_id, log_channel_id) VALUES({guild.id}, 0, 0)")
                db.commit()
                print(f'Guild {guild.name} added')
            
    
def get_greetings_channel(guild: disnake.Guild) -> int:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            return cursor.execute(f"SELECT greetings_channel_id FROM `guilds` WHERE guild_id = {guild.id}").fetchone()[0]
            
    
    
def get_log_channel(guild: disnake.Guild) -> int:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            return cursor.execute(f"SELECT log_channel_id FROM `guilds` WHERE guild_id = {guild.id}").fetchone()[0]


def set_greetings_channel_id(channel: disnake.TextChannel) -> None:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            cursor.execute(f"UPDATE `guilds` SET greetings_channel_id = {channel.id} WHERE guild_id = {channel.guild.id}")
            db.commit()
    
    
def set_log_channel_id(channel: disnake.TextChannel) -> None:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            cursor.execute(f"UPDATE `guilds` SET log_channel_id = {channel.id} WHERE guild_id = {channel.guild.id}")
            db.commit()


def get_user(user: disnake.Member) -> tuple:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            return cursor.execute(f"SELECT * FROM `users` WHERE user_id = {user.id}").fetchone()


def add_user(user: disnake.Member) -> None:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            cursor.execute(f"SELECT * FROM `users` WHERE user_id = {user.id}")
            if cursor.rowcount == 0:
                cursor.execute(f"INSERT INTO `users` (user_id, balance, xp, lvl) VALUES({user.id}, 0, 0, 1)")
                db.commit()
                print(f'User {user.name} added')


def get_balance(user: disnake.Member) -> int:
    return get_user(user)[1]
        
    
def get_xp(user: disnake.Member) -> int:
    return get_user(user)[2]


def get_lvl(user: disnake.Member) -> int:
    return get_user(user)[3]
    
    
def change_balance(user: disnake.Member, amount: int) -> None:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            balance = cursor.execute(f"SELECT balance FROM `users` WHERE user_id = {user.id}").fetchone()[1] + amount
            cursor.execute(f"UPDATE `users` SET balance = {balance} WHERE user_id = {user.id}")
            db.commit()
    
    
def change_xp(user: disnake.Member, amount: int) -> None:
    with closing(connect()) as db:
        with db.cursor(buffered=True) as cursor:
            result = cursor.execute(f"SELECT balance FROM `users` WHERE user_id = {user.id}").fetchone()
            xp = result[2] + amount
            lvl = result[3]
            if xp >= lvl * 50:
                xp -= lvl * 50
                lvl += 1
            cursor.execute(f"UPDATE `users` SET xp = {xp}, lvl = {lvl} WHERE user_id = {user.id}")
            db.commit()
      