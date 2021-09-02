from udemypy.tgm.text import emojis


get_course_button_text = f"Get course {emojis.PERSON_RUNNING}"

share_button_text = f"Share channel {emojis.SPEAKING_HEAD}"

donate_button_text = f"Donate me {emojis.HEART}"


def message_title(course_link, course_title) -> str:
    return f"[{emojis.TICKET}]({course_link}) _*Free Udemy Course:*_\n\n{course_title}"
