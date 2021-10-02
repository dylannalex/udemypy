from udemypy.udemy import courses
from udemypy.database import connection, db_management
from udemypy.tgm import tgm_bot


def main() -> None:
    # Scrape courses
    courses_found = courses.get_courses()

    # Add courses to database
    db = connection.connect_to_database()
    courses_added = db_management.add_courses(db, courses_found)

    # Send courses to Telegram channel
    dispatcher = tgm_bot.connect()
    for course in courses_added:
        tgm_bot.send_course(dispatcher, course)


if __name__ == "__main__":
    main()
