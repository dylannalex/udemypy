from udemypy.database import database
from udemypy.database import settings as db_settings
from udemypy.udemy import settings as ud_settings
from udemypy import settings
from udemypy.sender import SenderBot, TelegramBot, WhatsAppBot
from datetime import datetime


def get_bot(social_media_name: str) -> SenderBot:
    if social_media_name == db_settings.TELEGRAM_NAME:
        bot = TelegramBot(
            settings.TOKEN,
            settings.CHANNEL_ID,
            settings.CHANNEL_LINK,
            settings.GITHUB_LINK,
            settings.WHATSAPP_LINK,
        )

    if social_media_name == db_settings.WHATSAPP_NAME:
        bot = WhatsAppBot(ud_settings.CHROMEDRIVER_PATH)

    return bot


def send_courses(
    social_media_name: str,
    social_media_id: int,
) -> None:
    # Get new courses to share
    db: database.DataBase = database.connect()
    courses = database.retrieve_courses(db)
    courses_shared = database.retrieve_courses_shared_to_social_media(
        db,
        social_media_name,
    )
    courses_shared_id = [c.id for c in courses_shared]
    new_courses = [c for c in courses if c.id not in courses_shared_id]

    print(f"[-] {len(new_courses)} new courses to share!")

    if len(new_courses) == 0:
        return

    # Create bot
    bot = get_bot(social_media_name)
    bot.connect()

    # Share new courses
    for course_ in new_courses:
        print(f"\n\n[BOT] Sending course: {course_.title}")
        try:
            bot.send_course(course_)
        except Exception as exception:
            print(
                f"Could not send course to {social_media_name}",
                f"Course Title: {course_.title}",
                f"Error: {exception}",
                sep="\n",
            )
            continue
        database.add_course_social_media(
            db,
            course_.id,
            social_media_id,
            datetime.now(),
        )


if __name__ == "__main__":
    send_courses(db_settings.WHATSAPP_NAME, db_settings.WHATSAPP_ID)
