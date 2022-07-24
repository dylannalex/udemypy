from os.path import join
from udemypy.database import database
from udemypy.database import script
from mysql.connector.connection import MySQLConnection


def setup_tables(db: MySQLConnection):
    database.execute_script(db, script.get_path("create_tables.sql"))


def setup_database():
    db = database.connect()
    setup_tables(db)


if __name__ == "__main__":
    setup_database()
