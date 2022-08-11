from udemypy import course
from udemypy.database import database
from udemypy.udemy import course_handler


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


def clean_database() -> None:
    # Connect to database
    db = database.connect()

    # Find courses that are not free anymore
    courses = database.retrieve_courses(db)
    courses_with_stats = course_handler.add_courses_stats(courses)
    courses_to_remove = course_handler.delete_free_courses(courses_with_stats)

    # Remove courses from database
    _remove_courses(db, courses_to_remove)
    _notify_removed_courses(courses_to_remove)


if __name__ == "__main__":
    clean_database()
