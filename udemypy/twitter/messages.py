from udemypy.text import emojis


def get_tweet(
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
