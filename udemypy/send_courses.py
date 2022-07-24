from udemypy.tgm import tgm_bot
from udemypy.twitter import twitter_bot
from udemypy.udemy import course
from udemypy.udemy import course_handler
from udemypy.database import database


def _send_courses(courses: list[course.CourseWithStats]):
    # Connect to Twitter and Telegram API
    api = twitter_bot.connect()
    dispatcher = tgm_bot.connect()

    # Send courses
    for course in courses:
        print(f"[Sending] course: {course.title}")

        # Send course to Telegram
        try:
            tgm_bot.send_course(
                dispatcher, course.link, course.title, course.rating, course.students
            )
        except Exception as exception:
            print(f"Could not send course to Telegram\nERROR:{exception}")

        # Send course to Twitter
        try:
            twitter_bot.tweet_course(
                api, course.link, course.title, course.rating, course.students
            )
        except Exception as exception:
            print(f"Could not send course to Twitter\nERROR:{exception}")


def main():
    # Connect to database
    db = database.connect()

    # Retrieve shared courses
    shared_courses = database.retrieve_courses(db)
    shared_courses_id = [course_.id for course_ in shared_courses]

    # Find new courses
    new_courses = course_handler.new_courses(shared_courses_id)

    # Add courses to database
    for course_ in new_courses:
        database.add_course(
            db,
            course_.id,
            course_.title,
            course_.link,
            course_.coupon_code,
            course_.date_found,
        )

    # Send courses
    courses_with_stats = course_handler.add_courses_stats(new_courses[0:3])
    _send_courses(courses_with_stats)


if __name__ == "__main__":
    main()
