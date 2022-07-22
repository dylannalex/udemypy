import mysql.connector
from urllib.parse import urlparse
from udemypy.database.settings import CLEARDB_DATABASE_URL


def connect_to_database():
    dbc = urlparse(CLEARDB_DATABASE_URL)
    db = mysql.connector.connect(
        host=dbc.hostname,
        user=dbc.username,
        database=dbc.path.lstrip("/"),
        passwd=dbc.password,
    )
    return db
