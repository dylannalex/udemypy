from tests import _logs
from tests import _constants
from udemypy.database import database
from mysql.connector.connection import MySQLConnection


@_logs.test_function
def test_add_course(db: MySQLConnection) -> None:
    database.add_course(
        db,
        _constants.EXAMPLE_COURSE.id,
        _constants.EXAMPLE_COURSE.title,
        _constants.EXAMPLE_COURSE.link,
        _constants.EXAMPLE_COURSE.coupon_code,
        _constants.EXAMPLE_COURSE.date_found,
    )


@_logs.test_function
def test_retrieve_courses(db: MySQLConnection) -> None:
    courses = database.retrieve_courses(db)
    for course in courses:
        print(f"-> {course.title}")


@_logs.test_function
def test_remove_course(db: MySQLConnection) -> None:
    database.remove_course(db, _constants.EXAMPLE_COURSE.id)


def test_database() -> None:
    db = database.connect()
    test_add_course(db)
    test_retrieve_courses(db)
    test_remove_course(db)


if __name__ == "__main__":
    test_database()
