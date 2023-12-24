from tweepy import API
from tweepy import OAuthHandler
from udemypy.course import Course
from udemypy.sender.bot import SenderBot
from udemypy.sender.text import emojis


def _get_tweet(
    title, link, rating, students, language, discount_time_left, badge
) -> str:
    tweet = [
        f"{emojis.BOOKS} {title}",
        f"{emojis.STAR}{rating}/5",
        f"{emojis.PEOPLE_SILHOUETTE}{students} students",
        f"{emojis.GLOBE}{language}",
        f"{emojis.HOURGLASS}Free for {discount_time_left}",
        f"Follow me for more free Udemy courses {emojis.HEART}",
        f"{emojis.LINK}{link}",
    ]

    # Add course badge (if any)
    _badge_index = 1
    if badge:
        tweet.insert(_badge_index, f"{emojis.TROPHY}{badge}")

    return "\n\n".join(tweet)


class TwitterBot(SenderBot):
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def connect(self) -> None:
        auth = OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = API(auth)

    def send_course(self, course: Course) -> None:
        self.api.update_status(
            status=_get_tweet(
                course.title,
                course.link,
                course.rating,
                course.students,
                course.language,
                course.discount_time_left,
                course.badge,
            )
        )
