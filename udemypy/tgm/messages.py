from udemypy.text import emojis


get_course_button_text = f"Get course {emojis.PERSON_RUNNING}"

share_button_text = f"Share channel {emojis.SPEAKING_HEAD}"

donate_button_text = f"Donate me {emojis.HEART}"

twitter_button_text = f"Twitter {emojis.FRONT_FACING_CHICK}"


def message_title(title, link, rating, students, language, discount_time_left) -> str:
    message = (
        f"[{emojis.BOOKS}]({link}) {title}",
        f"{emojis.STAR} Rating: {rating}\/5",
        f"{emojis.PEOPLE_SILHOUETTE} Students: {students}",
        f"{emojis.GLOBE} Language: {language}",
        f"{emojis.HOURGLASS} Time left: {discount_time_left}",
        f"Subscribe for more free Udemy courses {emojis.HEART}",
    )
    return "\n\n".join(message)
