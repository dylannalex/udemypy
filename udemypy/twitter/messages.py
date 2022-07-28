from udemypy.text import emojis


def get_tweet(title, link, rating, students, language, discount_time_left) -> str:
    tweet = (
        f"{emojis.BOOKS} {title}",
        f"{emojis.LINK}Link: {link}",
        f"{emojis.STAR}Rating: {rating}/5",
        f"{emojis.PEOPLE_SILHOUETTE}Students: {students}",
        f"{emojis.GLOBE}Language: {language}",
        f"{emojis.HOURGLASS}Time left: {discount_time_left}",
        f"Follow me for more free Udemy courses {emojis.HEART}",
    )
    return "\n\n".join(tweet)
