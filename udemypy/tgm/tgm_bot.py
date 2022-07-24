import telegram
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext.dispatcher import Dispatcher
from udemypy.text import markdown_validation
from udemypy.tgm import settings
from udemypy.tgm import messages


def connect() -> Dispatcher:
    bot = telegram.Bot(token=settings.TOKEN)
    updater = Updater(bot.token, use_context=True)
    return updater.dispatcher


def send_course(
    dispatcher, course_link, course_title, course_rating, course_students
) -> None:
    course_title = markdown_validation.get_valid_text(course_title)
    course_rating = markdown_validation.get_valid_text(course_rating)
    course_students = markdown_validation.get_valid_text(course_students)

    get_course_button = InlineKeyboardButton(
        text=messages.get_course_button_text, url=course_link
    )

    share_button = InlineKeyboardButton(
        text=messages.share_button_text, url=settings.CHANNEL_LINK
    )

    twitter_button = InlineKeyboardButton(
        text=messages.twitter_button_text, url=settings.TWITTER_LINK
    )

    dispatcher.bot.sendMessage(
        parse_mode="MarkdownV2",
        text=messages.message_title(
            course_title, course_link, course_rating, course_students
        ),
        chat_id=settings.CHANNEL_ID,
        reply_markup=InlineKeyboardMarkup(
            [[get_course_button], [share_button, twitter_button]]
        ),
    )
