from tweepy import API
from tweepy import OAuthHandler
from udemypy.twitter import settings
from udemypy.twitter import messages


def connect() -> API:
    auth = OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    return API(auth)


def tweet_course(
    api, course_link, course_title, course_rating, course_students
) -> None:
    api.update_status(
        status=messages.get_tweet(
            course_title, course_link, course_rating, course_students
        )
    )
