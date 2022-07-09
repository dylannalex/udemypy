import telegram
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext.dispatcher import Dispatcher
from udemypy.text import markdown_validation
from udemypy.tgm import data, messages


def _connect() -> Dispatcher:
    bot = telegram.Bot(token=data.TOKEN)
    updater = Updater(bot.token, use_context=True)
    return updater.dispatcher


def _send_course(dispatcher, course) -> None:
    title = markdown_validation.get_valid_text(course["title"])
    link = course["link"]
    rating = markdown_validation.get_valid_text(course["rating"])
    students = markdown_validation.get_valid_text(course["students"])

    get_course_button = InlineKeyboardButton(
        text=messages.get_course_button_text, url=course["link"]
    )

    share_button = InlineKeyboardButton(
        text=messages.share_button_text, url=data.CHANNEL_LINK
    )

    twitter_button = InlineKeyboardButton(
        text=messages.twitter_button_text, url=data.TWITTER_LINK
    )

    dispatcher.bot.sendMessage(
        parse_mode="MarkdownV2",
        text=messages.message_title(title, link, rating, students),
        chat_id=data.CHANNEL_ID,
        reply_markup=InlineKeyboardMarkup(
            [[get_course_button], [share_button, twitter_button]]
        ),
    )


def send_courses(courses) -> None:
    dispatcher = _connect()
    for course in courses:
        _send_course(dispatcher, course)


def send_message(message, buttons=None, disable_web_page_preview=True) -> None:
    dispatcher = _connect()
    if buttons:
        dispatcher.bot.sendMessage(
            parse_mode="MarkdownV2",
            text=message,
            chat_id=data.CHANNEL_ID,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=disable_web_page_preview,
        )
    else:
        dispatcher.bot.sendMessage(
            parse_mode="MarkdownV2",
            text=message,
            chat_id=data.CHANNEL_ID,
            disable_web_page_preview=disable_web_page_preview,
        )
