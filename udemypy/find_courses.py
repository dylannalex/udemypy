from udemypy.udemy import courses
from udemypy.database import connection, db_management
from udemypy.send_courses import send_courses


def main() -> None:
    # Scrape courses
    courses_found = courses.get_courses()

    # Add courses to database
    db = connection.connect_to_database()
    courses_added = db_management.add_courses(db, courses_found)

    # Send courses
    send_courses(courses_added)


if __name__ == "__main__":
    main()
