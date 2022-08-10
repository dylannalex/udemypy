import mysql.connector
from urllib.parse import urlparse
from udemypy.database import settings
from udemypy.database import script
from udemypy import course

from mysql.connector.connection import MySQLConnection
from mysql.connector.connection import MySQLCursor
from mysql.connector.errors import OperationalError
from typing import Callable


def connect() -> MySQLConnection:
    dbc = urlparse(settings.DATABASE_URL)
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
def execute_script(
    db: MySQLConnection, filename: str, variables: dict = None
) -> MySQLCursor:
    sql_commands = script.read_script(filename, variables)
    cursor = db.cursor()

    # Execute commands
    for command in sql_commands:
        cursor.execute(command)
        # Save modifications on database (if any)
        if script.modifies_database_state(command):
            db.commit()

    # Save cursor output and close it
    cursor_output = [output for output in cursor]
    cursor.close()

    return cursor_output


def add_course(
    db: MySQLConnection,
    course_id: int,
    course_title: str,
    course_link: str,
    course_coupon: str,
    date_found: str,
    discount: int,
    discount_time_left: str,
    students: str,
    rating: str,
    language: str,
    badge: str,
) -> None:
    script_path = script.get_path("add_course.sql")
    variables = {
        "id_value": course_id,
        "title_value": course_title,
        "link_value": course_link,
        "coupon_code_value": course_coupon,
        "date_found_value": date_found,
        "discount_value": discount,
        "discount_time_left_value": discount_time_left,
        "students_value": students,
        "rating_value": rating,
        "lang_value": language,
        "badge_value": badge,
    }
    execute_script(db, script_path, variables)


def retrieve_courses(db: MySQLConnection) -> list[dict]:
    script_path = script.get_path("retrieve_courses.sql")
    courses = []
    for course_values in execute_script(db, script_path):
        courses.append(course.Course(*course_values))
    return courses


def remove_course(db: MySQLConnection, course_id: int) -> None:
    script_path = script.get_path("remove_course.sql")
    variables = {"id_value": course_id}
    execute_script(db, script_path, variables)
