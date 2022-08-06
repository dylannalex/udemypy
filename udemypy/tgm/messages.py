from udemypy.text import emojis


get_course_button_text = f"Get course {emojis.PERSON_RUNNING}"

share_button_text = f"Share channel {emojis.SPEAKING_HEAD}"

donate_button_text = f"Donate me {emojis.HEART}"

twitter_button_text = f"Free Courses on Twitter {emojis.FRONT_FACING_CHICK}"

github_repo_text = f"GitHub Repo {emojis.HAPPY_CAT}"


def message_title(
    title, link, rating, students, language, discount_time_left, badge
) -> str:
    message = [
        f"[{emojis.BOOKS}]({link}) {title}",
        f"{emojis.STAR} {rating}/5",
        f"{emojis.PEOPLE_SILHOUETTE} {students} students",
        f"{emojis.GLOBE} {language}",
        f"{emojis.HOURGLASS} Free for {discount_time_left}",
        f"Subscribe for more free Udemy courses {emojis.HEART}",
    ]

    # Add course badge (if any)
    _badge_index = 1
    if badge:
        message.insert(_badge_index, f"{emojis.TROPHY} {badge}")

    return "\n\n".join(message)
