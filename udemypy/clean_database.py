from datetime import datetime
from udemypy.database import connection
from udemypy.database import database
from udemypy.database.settings import COURSE_LIFETIME


def get_old_courses(courses) -> list:
    """
    returns list of courses which lifetime in database have expired
    """
    today = datetime.today()
    old_courses = []
    for course in courses:
        course_date = datetime.strptime(course["date"], "%Y-%m-%d")
        time_between_dates = today - course_date
        if time_between_dates.days >= COURSE_LIFETIME:
            old_courses.append(course)
    return old_courses


def main():
    db = connection.connect_to_database()
    courses = database.retrieve_courses(db.cursor())
    old_courses = get_old_courses(courses)
    database.remove_courses(db, old_courses)


if __name__ == "__main__":
    main()
