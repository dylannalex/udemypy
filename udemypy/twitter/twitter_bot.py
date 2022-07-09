from tweepy import OAuthHandler, API
from udemypy.twitter import data, messages


def _connect() -> API:
    auth = OAuthHandler(data.API_KEY, data.API_KEY_SECRET)
    auth.set_access_token(data.ACCESS_TOKEN, data.ACCESS_TOKEN_SECRET)
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
