import telegram
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext.dispatcher import Dispatcher
from udemypy.tgm import tgm_data
from udemypy.tgm.text import validation, messages


def connect() -> Dispatcher:
    bot = telegram.Bot(token=tgm_data.TOKEN)
    updater = Updater(bot.token, use_context=True)
    return updater.dispatcher


def send_course(dispatcher, course) -> None:
    course_title = validation.get_valid_msg(course["title"])
    course_link = course["link"]

    get_course_button = InlineKeyboardButton(
        text=messages.get_course_button_text, url=course["link"]
    )

    share_button = InlineKeyboardButton(
        text=messages.share_button_text, url=tgm_data.CHANNEL_LINK
    )

    donate_button = InlineKeyboardButton(
        text=messages.donate_button_text, url=tgm_data.DONATE_ME_LINK
    )

    dispatcher.bot.sendMessage(
        parse_mode="MarkdownV2",
        text=messages.message_title(course_link, course_title),
        chat_id=tgm_data.CHANNEL_ID,
        reply_markup=InlineKeyboardMarkup(
            [[get_course_button], [share_button, donate_button]]
        ),
    )
