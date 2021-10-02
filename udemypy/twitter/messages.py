from udemypy.text import emojis


def get_tweet(title, link) -> str:
    return f"{emojis.BOOKS} {title}\n\n{emojis.LINK}Link: {link}\n\nFollow me for more free Udemy courses {emojis.HEART}"
