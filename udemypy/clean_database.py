from udemypy.database import database
from udemypy.udemy import course_handler
from udemypy.udemy.course import CourseWithStats


def _notify_removed_courses(courses: list[CourseWithStats]) -> None:
    print(f"[Database cleanup] {len(courses)} courses removed")
    for course_ in courses:
        print(
            f"""
[Course Removed] Title: {course_.title}
                 Current Discount: {course_.discount}
                 Date found: {course_.date_found}
""",
            end="\n\n",
        )


def _remove_courses(db, courses: list[CourseWithStats]) -> None:
    for course_ in courses:
        database.remove_course(db, course_.id)


def clean_database() -> None:
    db = database.connect()
    courses = database.retrieve_courses(db)
    courses_with_stats = course_handler.add_courses_stats(courses)
    courses_to_remove = course_handler.delete_free_courses(courses_with_stats)
    _remove_courses(db, courses_to_remove)
    _notify_removed_courses(courses_to_remove)


if __name__ == "__main__":
    clean_database()
