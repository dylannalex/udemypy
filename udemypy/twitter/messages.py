from udemypy.text import emojis


def get_tweet(title, link, rating, students) -> str:
    tweet = (
        f"{emojis.BOOKS} {title}",
        f"{emojis.LINK}Link: {link}",
        f"{emojis.STAR}Rating: {rating}/5",
        f"{emojis.PEOPLE_SILHOUETTE}Students: {students}",
        f"Follow me for more free Udemy courses {emojis.HEART}",
    )
    return "\n\n".join(tweet)
