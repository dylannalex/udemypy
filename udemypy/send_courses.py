from udemypy.tgm import tgm_bot
from udemypy.twitter import twitter_bot


def send_courses(courses):
    try:
        tgm_bot.send_courses(courses)
    except Exception as exception:
        print(f"\n\nCould not complete Telegram sending process\nERROR:{exception}")

    try:
        twitter_bot.send_courses(courses)
    except Exception as exception:
        print(f"\n\nCould not complete Twitter sending process\nERROR:{exception}")
