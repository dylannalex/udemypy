from udemypy.udemy import course_handler
from udemypy.database import database
from udemypy.send_courses import send_courses


def main() -> None:
    # Connect to database
    db = database.connect()

    # Retrieve shared courses
    shared_courses = database.retrieve_courses(db)
    shared_courses_titles = [course["title"] for course in shared_courses]

    # Find new courses
    new_courses = course_handler.get_new_courses(shared_courses_titles)

    # Add courses to database
    database.add_courses(db, new_courses)

    # Send courses
    send_courses(new_courses)


if __name__ == "__main__":
    main()
