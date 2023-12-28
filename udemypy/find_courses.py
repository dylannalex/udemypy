from udemypy import course
from udemypy.udemy import course_handler
from udemypy.database import database


def _save_courses(db, courses: list[course.Course]):
    for course_ in courses:
        try:
            database.add_course(
                db,
                course_.id,
                course_.title,
                course_.link,
                course_.coupon_code,
                course_.date_found,
                course_.discount,
                course_.discount_time_left,
                course_.students,
                course_.rating,
                course_.language,
                course_.badge,
            )
        except Exception as exception:
            print(
                f"[Database] Could not save course {course_.title}\nERROR: {exception}"
            )


def find_courses(db: database.DataBase, verbose: bool):
    # Retrieve shared courses
    courses_on_database = database.retrieve_courses(db)

    if verbose:
        print(f"[-] {len(courses_on_database)} courses on database")

    # Find new free courses with their stats
    new_courses = course_handler.new_courses(courses_on_database)

    if verbose:
        print(f"[-] {len(new_courses)} new courses found")

    courses_with_stats = course_handler.add_courses_stats(new_courses)
    free_courses = course_handler.delete_non_free_courses(courses_with_stats)

    # Add courses to database
    _save_courses(db, free_courses)


if __name__ == "__main__":
    find_courses(True)
