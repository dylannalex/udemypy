import mysql.connector
from urllib.parse import urlparse
from udemypy.database import settings

from mysql.connector.connection import MySQLConnection
from mysql.connector.errors import OperationalError
from typing import Callable


def connect() -> MySQLConnection:
    dbc = urlparse(settings.CLEARDB_DATABASE_URL)
    db = mysql.connector.connect(
        host=dbc.hostname,
        user=dbc.username,
        database=dbc.path.lstrip("/"),
        passwd=dbc.password,
    )
    return db


def database_access(function: Callable):
    def wrapper(db: MySQLConnection, *args):
        for _ in range(settings.RECONNECTION_ATTEMPTS):
            try:
                return function(db, *args)
            except OperationalError:
                db.reconnect()

    return wrapper


@database_access
def add_courses(db: MySQLConnection, courses: dict) -> list:
    cursor = db.cursor()
    courses_added = []
    for course in courses:
        print(f'COURSE: {course["title"]}')
        try:
            cursor.execute(
                f"""INSERT INTO {settings.TABLE_NAME} VALUES('{course['title']}', '{course['link']}', '{course['date']}');"""
            )
            print("SUCCESSFULLY ADDED\n")
            courses_added.append(course)

        except Exception as exception:
            print(f"FAILED - {exception}\n")

    db.commit()
    return courses_added


@database_access
def retrieve_courses(db: MySQLConnection) -> list[dict]:
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {settings.TABLE_NAME}")
    courses_added = []
    for row in cursor:
        courses_added.append(
            {"title": row[0], "link": row[1], "date": row[2].strftime("%Y-%m-%d")}
        )
    return courses_added


@database_access
def remove_courses(db: MySQLConnection, courses: dict) -> None:
    cursor = db.cursor()
    for course in courses:
        cursor.execute(
            f"""DELETE FROM {settings.TABLE_NAME} WHERE title='{course['title']}';"""
        )
    db.commit()
