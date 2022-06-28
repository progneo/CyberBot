import mysql.connector
import cyberbot

def __init__():
    try:
        database = mysql.connector.connect(
            host=cyberbot.config.db_host(),
            db=cyberbot.config.db_database(),
            user=cyberbot.config.db_user(),
            passwd=cyberbot.config.db_password()
        )
        return (database)
    except Exception as error:
        print("\nUnable to connect to database. Please check your credentials!\n" + str(error) + "\n")
        quit()


def db(database):
    try:
        return database.cursor(buffered=True)
    except Exception as e:
        print(f"\nAn error occurred while executing SQL statement\n{e}\n")
        quit()


def create_table(stmt):
    database = cyberbot.managers.database.__init__()
    db = cyberbot.managers.database.db(database)

    db.execute(stmt)
    db.close()
    del db


def insert(stmt, var):
    database = cyberbot.managers.database.__init__()
    db = cyberbot.managers.database.db(database)

    db.execute(stmt, var)
    database.commit()

    db.close()
    del db


def insert_if_not_exists(stmt):
    database = cyberbot.managers.database.__init__()
    db = cyberbot.managers.database.db(database)

    db.execute(stmt)
    database.commit()

    db.close()
    del db


def create_guild_table(guild):
    database = cyberbot.managers.database.__init__()
    db = cyberbot.managers.database.db(database)

    db.execute("SELECT * FROM `guilds` WHERE guild_id = '" + str(guild.id) + "'")
    if db.rowcount == 0:
        insert("INSERT INTO `guilds`(guild_id, guild_name) VALUES(%s, %s)", (guild.id, guild.name))