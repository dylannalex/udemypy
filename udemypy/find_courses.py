from udemypy.udemy import courses
from udemypy.database import database
from udemypy.send_courses import send_courses


def main() -> None:
    # Scrape courses
    courses_found = courses.get_courses()

    # Add courses to database
    db = database.connect()
    courses_added = database.add_courses(db, courses_found)

    # Send courses
    send_courses(courses_added)


if __name__ == "__main__":
    main()
