from udemypy import course
from udemypy.tgm import tgm_bot
from udemypy.twitter import twitter_bot
from udemypy.database import database
from udemypy.database import settings as db_settings

from datetime import datetime

from mysql.connector.connection import MySQLConnection
from typing import Callable, Any


def sender(function: Callable):
    def wrapper(*args: Any):
        db: MySQLConnection = database.connect()
        courses = database.retrieve_courses(db)
        print(f"[Starting Bot] Running {function.__name__}()")
        function(db, courses, *args)

    return wrapper


@sender
def send_courses_to_telegram(db: MySQLConnection, courses: list[course.Course]):
    # Get new courses
    courses_shared_to_telegram = database.retrieve_courses_shared_to_telegram(db)
    courses_shared_to_telegram_ids = [c.id for c in courses_shared_to_telegram]
    new_courses = [c for c in courses if c.id not in courses_shared_to_telegram_ids]

    # Send courses to Telegram
    dispatcher = tgm_bot.connect()
    for course_ in new_courses:
        print(f"[Sending] course: {course_.title}")
        try:
            tgm_bot.send_course(
                dispatcher,
                course_.link_with_coupon,
                course_.title,
                course_.rating,
                course_.students,
                course_.language,
                course_.discount_time_left,
                course_.badge,
            )
        except Exception as exception:
            print(
                "[Telegram Bot] Could not send course to Telegram",
                f"Course Title: {course_.title}",
                f"Error: {exception}",
                sep="\n",
            )
            continue
        try:
            database.add_course_social_media(
                db,
                course_.id,
                db_settings.TELEGRAM_ID,
                datetime.now(),
            )
        except Exception as exception:
            print(
                "[Database] Could not save course shared to Telegram",
                f"Course Title: {course_.title}",
                f"Error: {exception}",
                sep="\n",
            )


@sender
def send_courses_to_twitter(db: MySQLConnection, courses: list[course.Course]):
    # Get new courses
    courses_shared_to_twitter = database.retrieve_courses_shared_to_twitter(db)
    courses_shared_to_twitter_ids = [c.id for c in courses_shared_to_twitter]
    new_courses = [c for c in courses if c.id not in courses_shared_to_twitter_ids]

    # Send courses to Twitter
    api = twitter_bot.connect()
    for course_ in new_courses:
        print(f"[Sending] course: {course_.title}")
        # Send course to Telegram
        try:
            twitter_bot.tweet_course(
                api,
                course_.link_with_coupon,
                course_.title,
                course_.rating,
                course_.students,
                course_.language,
                course_.discount_time_left,
                course_.badge,
            )
        except Exception as exception:
            print(
                "[Twitter Bot] Could not send course to Twitter",
                f"Course Title: {course_.title}",
                f"Error: {exception}",
                sep="\n",
            )
            continue
        try:
            database.add_course_social_media(
                db,
                course_.id,
                db_settings.TWITTER_ID,
                datetime.now(),
            )
        except Exception as exception:
            print(
                "[Database] Could not save course shared to Twitter",
                f"Course Title: {course_.title}",
                f"Error: {exception}",
                sep="\n",
            )


def send_courses():
    send_courses_to_telegram()
    send_courses_to_twitter()


if __name__ == "__main__":
    send_courses()
