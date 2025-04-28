from time import sleep
from abc import abstractmethod
from abc import ABC
from datetime import datetime, timedelta

from udemypy import send_courses
from udemypy import find_courses
from udemypy.database import database
from udemypy.database import settings as db_settings
from udemypy.udemy import settings as ud_settings
from udemypy import settings
from udemypy.sender import TelegramBot, WhatsAppBot
from udemypy.utils import clear_console


class BotHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def send_courses(self, verbose: bool):
        pass


class TelegramHandler(BotHandler):
    def __init__(self):
        self.bot = TelegramBot(
            settings.TOKEN,
            settings.CHANNEL_ID,
            settings.CHANNEL_LINK,
            settings.GITHUB_LINK,
            settings.WHATSAPP_LINK,
        )

    def send_courses(self, db):
        print("[Telegram Bot]")
        self.bot.connect()  # Reconnects every iteration
        send_courses.send_courses(
            db,
            self.bot,
            db_settings.TELEGRAM_NAME,
            db_settings.TELEGRAM_ID,
        )


class WhatsAppHandler(BotHandler):
    def __init__(self):
        self.whatsapp_bot = WhatsAppBot(ud_settings.CHROMEDRIVER_PATH)
        self.whatsapp_bot.connect()  # Only first connection

    def send_courses(self, db):
        # WhatsApp Bot
        print("[WhatsApp Bot]")
        send_courses.send_courses(
            db,
            self.bot,
            db_settings.WHATSAPP_NAME,
            db_settings.WHATSAPP_ID,
        )


def schedule_bots(
    bot_handlers: list[BotHandler],
    waiting_seconds: int,
    iterations: int,
):
    db = database.connect()
    waiting_seconds = 60 * 30  # 30 min
    iterations = 10

    for iteration in range(iterations):
        # Find courses
        clear_console()
        print(f"[Iteration N°{iteration}]")
        print("[Finding Courses]")
        find_courses.find_courses(db, verbose=True)

        # Send courses
        for bot_handler in bot_handlers:
            bot_handler.send_courses(db)

        # Calculate the time of the next iteration
        next_iteration_time = datetime.now() + timedelta(seconds=waiting_seconds)
        next_iteration_time = next_iteration_time.strftime("%H:%M:%S")
        print(f"\n[-] Next iteration at: {next_iteration_time}")

        # Sleep
        sleep(waiting_seconds)

    db.close()


if __name__ == "__main__":
    schedule_bots(
        bot_handlers=[TelegramHandler()],
        waiting_seconds=60 * 30,
        iterations=20,
    )
