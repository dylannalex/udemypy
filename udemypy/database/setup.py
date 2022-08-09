from os.path import join
from udemypy.database import database
from udemypy.database import script
from mysql.connector.connection import MySQLConnection


def setup_database():
    db: MySQLConnection = database.connect()
    database.execute_script(db, script.get_path("create_tables.sql"))
    database.execute_script(db, script.get_path("setup_tables.sql"))


if __name__ == "__main__":
    setup_database()
