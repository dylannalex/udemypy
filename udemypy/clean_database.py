import os
from enum import Enum

from udemypy import course
from udemypy.database import database
from udemypy.database import settings as db_setts
from udemypy.udemy import course_handler


class CleaningStrategy(Enum):
    OLD = 1
    NON_FREE = 2


def _notify_removed_courses(courses: list[course.Course]) -> None:
    print(f"[Database cleanup] {len(courses)} courses removed")
    for course_ in courses:
        print(
            f"""
[Course Removed] Title: {course_.title}
                 Current Discount: {course_.discount}
                 Date found: {course_.date_found}""",
            end="\n\n",
        )


def _remove_courses(db, courses: list[course.Course]) -> None:
    for course_ in courses:
        database.remove_course(db, course_.id)


def clean_database(strategies: list[CleaningStrategy]) -> None:
    # Connect to database and retrieve courses
    db = database.connect()
    courses = database.retrieve_courses(db)
    courses_to_remove = []
    os.system("cls")
    print(f"[Stats] Courses on database: {len(courses)}")

    # Find courses to remove
    for strategy in strategies:
        if strategy == CleaningStrategy.NON_FREE:
            # Find courses that are not free anymore
            courses_with_stats = course_handler.add_courses_stats(courses)
            to_remove = course_handler.delete_free_courses(courses_with_stats)
            courses_to_remove.extend(to_remove)
            print(f"[Non Free Strategy] Found {len(to_remove)} courses to remove")

        if strategy == CleaningStrategy.OLD:
            # Find old courses
            to_remove = course_handler.delete_old_courses(
                courses, db_setts.COURSE_LIFETIME
            )
            courses_to_remove.extend(to_remove)
            print(f"[Old Course Strategy] Found {len(to_remove)} courses to remove")

    # Remove duplicates
    courses_to_remove = list(dict.fromkeys(courses_to_remove))

    # Remove courses from database
    _remove_courses(db, courses_to_remove)
    _notify_removed_courses(courses_to_remove)


if __name__ == "__main__":
    clean_database([CleaningStrategy.OLD])
