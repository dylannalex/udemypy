import telegram
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext.dispatcher import Dispatcher
from udemypy.text import markdown_validation
from udemypy.tgm import data, messages


def connect() -> Dispatcher:
    bot = telegram.Bot(token=data.TOKEN)
    updater = Updater(bot.token, use_context=True)
    return updater.dispatcher


def send_course(dispatcher, course) -> None:
    course_title = markdown_validation.get_valid_text(course["title"])
    course_link = course["link"]

    get_course_button = InlineKeyboardButton(
        text=messages.get_course_button_text, url=course["link"]
    )

    share_button = InlineKeyboardButton(
        text=messages.share_button_text, url=data.CHANNEL_LINK
    )

    donate_button = InlineKeyboardButton(
        text=messages.donate_button_text, url=data.DONATE_ME_LINK
    )

    dispatcher.bot.sendMessage(
        parse_mode="MarkdownV2",
        text=messages.message_title(course_link, course_title),
        chat_id=data.CHANNEL_ID,
        reply_markup=InlineKeyboardMarkup(
            [[get_course_button], [share_button, donate_button]]
        ),
    )
