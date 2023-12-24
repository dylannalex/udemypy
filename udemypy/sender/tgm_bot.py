import telegram
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext.dispatcher import Dispatcher
from udemypy.course import Course
from udemypy.sender.text import markdown_validation
from udemypy.sender.text import emojis
from udemypy.sender.bot import SenderBot


def _message_title(
    title, link, rating, students, language, discount_time_left, badge
) -> str:
    message = [
        f"[{emojis.BOOKS}]({link}) {title}",
        f"{emojis.STAR} {rating}/5",
        f"{emojis.PEOPLE_SILHOUETTE} {students} students",
        f"{emojis.GLOBE} {language}",
        f"{emojis.HOURGLASS} Free for {discount_time_left}",
        f"Subscribe for more free Udemy courses {emojis.HEART}",
    ]

    # Add course badge (if any)
    _badge_index = 1
    if badge:
        message.insert(_badge_index, f"{emojis.TROPHY} {badge}")

    return "\n\n".join(message)


class TelegramBot(SenderBot):
    get_course_button_text = f"Get course {emojis.PERSON_RUNNING}"
    share_button_text = f"Share channel {emojis.SPEAKING_HEAD}"
    donate_button_text = f"Donate me {emojis.HEART}"
    twitter_button_text = f"Free Courses on Twitter {emojis.FRONT_FACING_CHICK}"
    github_repo_text = f"GitHub Repo {emojis.HAPPY_CAT}"

    def __init__(
        self, token: str, channel_id: str, channel_link: str, github_link: str
    ):
        self.token = token
        self.channel_id = channel_id
        self.channel_link = channel_link
        self.github_link = github_link

    def connect(self) -> None:
        bot = telegram.Bot(token=self.token)
        updater = Updater(bot.token, use_context=True)
        self.dispatcher: Dispatcher = updater.dispatcher

    def send_course(self, course: Course) -> None:
        course_title = markdown_validation.get_valid_text(course.title)
        course_rating = markdown_validation.get_valid_text(course.rating)
        course_students = markdown_validation.get_valid_text(course.students)

        get_course_button = InlineKeyboardButton(
            text=__class__.get_course_button_text, url=course.link
        )

        share_button = InlineKeyboardButton(
            text=__class__.share_button_text, url=self.channel_link
        )

        # twitter_button = InlineKeyboardButton(
        # text=messages.twitter_button_text, url=self.twitter_link
        # )

        github_button = InlineKeyboardButton(
            text=__class__.github_repo_text, url=self.github_link
        )

        self.dispatcher.bot.sendMessage(
            parse_mode="MarkdownV2",
            text=_message_title(
                course_title,
                course.link,
                course_rating,
                course_students,
                course.language,
                course.discount_time_left,
                course.badge,
            ),
            chat_id=self.channel_id,
            reply_markup=InlineKeyboardMarkup(
                [[get_course_button], [share_button, github_button]],
            ),
        )
