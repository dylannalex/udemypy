from tweepy import API
from tweepy import OAuthHandler
from udemypy.twitter import settings
from udemypy.twitter import messages


def _connect() -> API:
    auth = OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    return API(auth)


def _tweet_course(api, course) -> None:
    api.update_status(
        status=messages.get_tweet(
            course["title"], course["link"], course["rating"], course["students"]
        )
    )


def send_courses(courses) -> None:
    api = _connect()
    for course in courses:
        try:
            _tweet_course(api, course)
        except Exception as exception:
            print(f"\n\nCould not tweet course: {course['title']}\nERROR: {exception}")
