from udemypy import send_courses
from udemypy import find_courses
from udemypy.database import database
from udemypy.database import settings as db_settings
from udemypy.udemy import settings as ud_settings
from udemypy import settings
from udemypy.sender import TelegramBot, WhatsAppBot
from datetime import datetime, timedelta
from time import sleep
from os import system


def schedule():
    db = database.connect()
    whatsapp_bot = WhatsAppBot(ud_settings.CHROMEDRIVER_PATH)
    whatsapp_bot.connect()
    telegram_bot = TelegramBot(
        settings.TOKEN,
        settings.CHANNEL_ID,
        settings.CHANNEL_LINK,
        settings.GITHUB_LINK,
        settings.WHATSAPP_LINK,
    )
    waiting_time = 60 * 30  # 30 min
    iterations = 10

    for iteration in range(iterations):
        # Find courses
        system("cls")
        print(f"[Iteration N°{iteration}]")
        print("[Finding Courses]")
        find_courses.find_courses(db, verbose=True)

        # Telegram Bot
        print("[Telegram Bot]")
        telegram_bot.connect()  # Reconnects every iteration
        send_courses.send_courses(
            db,
            telegram_bot,
            db_settings.TELEGRAM_NAME,
            db_settings.TELEGRAM_ID,
        )

        # WhatsApp Bot
        print("[WhatsApp Bot]")
        send_courses.send_courses(
            db,
            whatsapp_bot,
            db_settings.WHATSAPP_NAME,
            db_settings.WHATSAPP_ID,
        )

        # Calculate the time of the next iteration
        next_iteration_time = datetime.now() + timedelta(seconds=waiting_time)
        next_iteration_time = next_iteration_time.strftime("%H:%M:%S")
        print(f"\n[-] Next iteration at: {next_iteration_time}")

        # Sleep
        sleep(waiting_time)

    db.close()


if __name__ == "__main__":
    schedule()
