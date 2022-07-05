import disnake
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from cyberbot import config

class Database():
    __slots__ = ['database', 'bot']
        
    def __init__(self, bot):
        try:
            self.bot: disnake.Client = bot
            self.database: MySQLConnection = mysql.connector.connect(
                host=config.db_host(),
                db=config.db_database(),
                user=config.db_user(),
                passwd=config.db_password()
            )
        except Exception as error:
            print("\nUnable to connect to database. Please check your credentials!\n" + str(error) + "\n")
            quit()

    async def get_cursor(self) -> MySQLCursor:
        try:
            return self.database.cursor(buffered=True)
        except Exception as e:
            print(f"\nAn error occurred while executing SQL statement\n{e}\n")
            quit()

    async def insert(self, stmt, var) -> None:
        cursor = self.get_cursor(self.database)

        cursor.execute(stmt, var)
        self.database.commit()

        cursor.close()
        del cursor

    async def create_tables(self) -> None:
        cursor = self.get_cursor()
        
        cursor.execute('CREATE TABLE IF NOT EXISTS `guilds` (`guild_id` BIGINT, `greetings_channel_id` BIGINT, `log_channel_id` BIGINT)')
        cursor.execute("CREATE TABLE IF NOT EXISTS `users` (`user_id` BIGINT, `balance` BIGINT, `xp` INT, `lvl` INT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS `bot_logs` (`timestamp` TEXT, `type` TINYTEXT, `class` TINYTEXT, `message` MEDIUMTEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS `guild_logs` (`timestamp` TEXT, `guild_id` BIGINT, `channel_id` BIGINT, `message_id` BIGINT, `user_id` BIGINT, `action_type` TINYTEXT, `message` MEDIUMTEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS `blacklist` (`guild_id` BIGINT, `user_id` BIGINT, `reason` MEDIUMTEXT)")

        self.database.commit()
        
        cursor.close()
        del cursor

    async def add_guild(self, guild) -> None:
        cursor = self.get_cursor()

        cursor.execute(f"SELECT * FROM `guilds` WHERE guild_id = {guild.id}")
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO `guilds`(guild_id, guild_name) VALUES(%s, %s)", (guild.id, guild.name))
            
        self.database.commit()
        
        cursor.close()
        del cursor
        
    async def get_xp(self, user) -> int:
        pass
    
    async def get_lvl(self, user) -> int:
        pass
    
    async def get_balance(self, user) -> int:
        pass
        
    async def change_balance(self, user, amount) -> None:
        cursor = self.get_cursor()
        
        new_balance = await self.get_balance(user) + amount
        cursor.execute('')
        
        self.database.commit()
        
        cursor.close()
        del cursor
        
    async def increace_xp(self, user, xp) -> None:
        cursor = self.get_cursor()
        
        new_xp = await self.get_xp(user) + xp
        cursor.execute('')
        
        self.database.commit()
        
        cursor.close()
        del cursor
        
    async def increace_lvl(self, user) -> None:
        cursor = self.get_cursor()
        
        new_lvl = await self.get_lvl(user) + 1
        cursor.execute('')
        
        self.database.commit()
        
        cursor.close()
        del cursor        
        
    async def get_greetings_channel(self, guild: disnake.Guild) -> disnake.TextChannel:
        cursor = self.get_cursor()
        
        channel_id = cursor.execute('')
        cursor.close()
        del cursor    
        
        channel: disnake.TextChannel = None
        
        if channel_id != 0:
            channel = self.bot.get_channel()
        
        return channel
        
    async def get_log_channel(self, guild: disnake.Guild) -> disnake.TextChannel:
        cursor = self.get_cursor()
        
        channel_id = cursor.execute('')
        cursor.close()
        del cursor    
        
        channel: disnake.TextChannel = None
        
        if channel_id != 0:
            channel = self.bot.get_channel()
        
        return channel
    
    async def set_greetings_channel_id(self, channel: disnake.TextChannel) -> None:
        pass
        
    async def set_log_channel_id(self, channel: disnake.TextChannel) -> None:
        pass