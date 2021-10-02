from udemypy.tgm import tgm_bot
from udemypy.twitter import twitter_bot


def send_courses(courses):
    tgm_bot.send_courses(courses)
    twitter_bot.send_courses(courses)
