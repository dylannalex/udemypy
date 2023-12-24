from udemypy.database import database
from udemypy.database import settings as db_settings
from udemypy import settings
from udemypy.sender import SenderBot, TelegramBot
from datetime import datetime


def send_courses(platform: str) -> None:
    db: database.DataBase = database.connect()
    courses = database.retrieve_courses(db)

    if platform == "telegram":
        # Find courses that were not send to Telegram
        courses_shared_to_telegram = database.retrieve_courses_shared_to_telegram(db)
        courses_shared_to_telegram_ids = [c.id for c in courses_shared_to_telegram]
        new_courses = [c for c in courses if c.id not in courses_shared_to_telegram_ids]

        # Create bot
        bot: SenderBot = TelegramBot(
            settings.TOKEN,
            settings.CHANNEL_ID,
            settings.CHANNEL_LINK,
            settings.GITHUB_LINK,
        )

    bot.connect()

    for course_ in new_courses:
        print(f"\n\n[BOT] Sending course: {course_.title}")
        try:
            bot.send_course(course_)
        except Exception as exception:
            print(
                f"Could not send course to {platform}",
                f"Course Title: {course_.title}",
                f"Error: {exception}",
                sep="\n",
            )
            continue
        database.add_course_social_media(
            db,
            course_.id,
            db_settings.TELEGRAM_ID,
            datetime.now(),
        )


if __name__ == "__main__":
    send_courses("telegram")
